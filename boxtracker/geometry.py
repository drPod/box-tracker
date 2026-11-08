"""Stick pose from two coloured bands plus the known pivot, and the sim pose conventions."""
import math

import cv2
import numpy as np


def unit(v):
    return v / np.linalg.norm(v)


def port_frame(port):
    """Nominal trocar axes, exactly as the sim's tools.js `Tl()` builds them."""
    o = np.asarray(port["pos"], float)
    d = unit(np.asarray(port["aim"], float) - o)
    r = np.cross(d, [0.0, 1.0, 0.0])
    if np.linalg.norm(r) < 1e-6:
        r = np.array([1.0, 0, 0])
    r = unit(r)
    u = np.cross(r, d)
    return o, d, r, u


def sim_angles(port, direction):
    """Inward shaft direction (sim frame) -> (yaw, pitch) like the sim's `Dl()`."""
    _, d, r, u = port_frame(port)
    a = unit(np.asarray(direction, float))
    pitch = math.asin(max(-1.0, min(1.0, float(a @ u))))
    yaw = math.atan2(float(a @ r), float(a @ d))
    return yaw, pitch


def sim_direction(port, yaw, pitch):
    """Inverse of sim_angles (the sim's `El()` shaft direction)."""
    _, d, r, u = port_frame(port)
    return unit(d * math.cos(pitch) * math.cos(yaw) + r * math.cos(pitch) * math.sin(yaw)
                + u * math.sin(pitch))


class Camera:
    """Pinhole camera with lid pose. Points in the lid frame -> pixels."""

    def __init__(self, K, dist, rvec=None, tvec=None):
        self.K = np.asarray(K, float)
        self.dist = np.asarray(dist, float).ravel()
        self.set_pose(rvec, tvec)

    def set_pose(self, rvec, tvec):
        self.rvec = None if rvec is None else np.asarray(rvec, float).reshape(3)
        self.tvec = None if tvec is None else np.asarray(tvec, float).reshape(3)
        if self.rvec is not None:
            self.R = cv2.Rodrigues(self.rvec)[0]
        else:
            self.R = None

    @property
    def posed(self):
        return self.R is not None

    def to_cam(self, X_lid):
        return np.asarray(X_lid, float) @ self.R.T + self.tvec

    def project(self, X_lid):
        X = np.atleast_2d(np.asarray(X_lid, float))
        pts, _ = cv2.projectPoints(X, self.rvec, self.tvec, self.K, self.dist)
        return pts.reshape(-1, 2)

    def normalize(self, px):
        """Pixels -> undistorted normalized image coordinates."""
        px = np.asarray(px, float).reshape(-1, 1, 2)
        return cv2.undistortPoints(px, self.K, self.dist).reshape(-1, 2)

    def lid_pixels_per_metre(self, X_lid):
        p0 = self.project(X_lid)[0]
        p1 = self.project(np.asarray(X_lid) + [0.01, 0, 0])[0]
        p2 = self.project(np.asarray(X_lid) + [0, 0.01, 0])[0]
        return 50 * (np.linalg.norm(p1 - p0) + np.linalg.norm(p2 - p0))


class StickSolver:
    """Find the outward stick direction v and the pivot->band2 distance s.

    band2 = P + s v, band1 = P + (s + L) v, with P the pivot (all in camera coords).
    Minimises reprojection error of both band centres with a tiny Levenberg-Marquardt.
    """

    def __init__(self, cam, pivot_lid, spacing, max_tilt_deg=75):
        self.cam = cam
        self.P = cam.to_cam(pivot_lid)
        self.z_lid = cam.R[:, 2]          # lid normal (up) in camera coords
        self.L = spacing
        self.fx = cam.K[0, 0]
        self.min_up = math.cos(math.radians(max_tilt_deg))

    def residual(self, v, s, n2, n1):
        X2 = self.P + s * v
        X1 = self.P + (s + self.L) * v
        if X2[2] <= 1e-4 or X1[2] <= 1e-4:
            return np.full(4, 1e3)
        return self.fx * np.concatenate([X2[:2] / X2[2] - n2, X1[:2] / X1[2] - n1])

    def _lm(self, v, s, n2, n1, iters=12):
        lam = 1e-3
        r = self.residual(v, s, n2, n1)
        cost = r @ r
        for _ in range(iters):
            # local tangent basis around v
            a = np.cross(v, [1.0, 0, 0])
            if np.linalg.norm(a) < 0.1:
                a = np.cross(v, [0, 1.0, 0])
            a = unit(a)
            b = np.cross(v, a)

            def f(x):
                return self.residual(unit(v + x[0] * a + x[1] * b), s + x[2], n2, n1)
            J = np.empty((4, 3))
            h = (1e-5, 1e-5, 1e-5)
            for k in range(3):
                dx = np.zeros(3)
                dx[k] = h[k]
                J[:, k] = (f(dx) - r) / h[k]
            A = J.T @ J
            g = J.T @ r
            while True:
                step = -np.linalg.solve(A + lam * np.diag(np.diag(A) + 1e-9), g)
                v_new = unit(v + step[0] * a + step[1] * b)
                s_new = max(0.0, s + step[2])
                r_new = self.residual(v_new, s_new, n2, n1)
                c_new = r_new @ r_new
                if c_new < cost:
                    v, s, r, cost = v_new, s_new, r_new, c_new
                    lam = max(lam / 3, 1e-7)
                    break
                lam *= 4
                if lam > 1e6:
                    return v, s, cost
            if np.linalg.norm(step) < 1e-7:
                break
        return v, s, cost

    def solve(self, px2, px1, prev=None):
        """px2/px1: pixel centres of band2 (lower) and band1. Returns (v_cam, s, rms_px)."""
        n = self.cam.normalize(np.array([px2, px1]))
        n2, n1 = n[0], n[1]
        inits = []
        if prev is not None:
            inits.append(prev)
        z = self.z_lid
        x = self.cam.R[:, 0]
        y = self.cam.R[:, 1]
        for tilt in (0.0, 0.5):
            for az in ((0,) if tilt == 0 else (0, math.pi / 2, math.pi, 3 * math.pi / 2)):
                v0 = unit(z * math.cos(tilt) + math.sin(tilt) * (x * math.cos(az) + y * math.sin(az)))
                inits.append((v0, 0.06))
        best = None
        for i, (v0, s0) in enumerate(inits):
            v, s, cost = self._lm(np.asarray(v0, float), float(s0), n2, n1)
            if v @ z < self.min_up:
                continue
            if best is None or cost < best[2]:
                best = (v, s, cost)
            if i == 0 and prev is not None and cost < 4 * 1.0:   # warm start good enough
                break
        if best is None:
            return None
        v, s, cost = best
        return v, s, math.sqrt(cost / 4)

    def lid_direction(self, v_cam):
        return self.cam.R.T @ v_cam
