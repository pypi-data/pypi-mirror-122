"""
Developed by: Ide Govers, Junzi Sun
March 2021
"""

import casadi as ca
import numpy as np
import matplotlib.pyplot as plt
from openap.casadi import prop, aero, Drag, FuelFlow, nav, WRAP


class EOM:
    def dx(v, psi, gamma, xp, yp, h, wind_features):
        """Function to find the xpos time derivative (m)

        v:          true airspeed in m/s.
        psi:        heading angle (deg).
        gamma:      flight path angle (deg).
        xp:         x position relative to dep (m).
        yp:         y position relative to dep (m).
        h:          altitude (m)

        """

        xdot = v * ca.sin(psi * ca.pi / 180) * ca.cos(gamma * ca.pi / 180)
        return xdot

    def dy(v, psi, gamma, xp, yp, h, wind_features):
        """Function to find the ypos time derivative (m)

        v:          true airspeed in m/s.
        psi:        heading angle (deg).
        gamma:      flight path angle (deg).
        xp:         x position relative to dep (m).
        yp:         y position relative to dep (m).
        h:          altitude (m)

        """
        ydot = v * ca.cos(psi * ca.pi / 180) * ca.cos(gamma * ca.pi / 180)
        return ydot

    def dh(v, gamma):
        """Function to find the altitude time derivative (m)

        v:          true airspeed in m/s
        gamma:      flight path angle (deg)

        """

        zdot = v * ca.sin(gamma * ca.pi / 180)
        return zdot

    def dv(v, m, h, T, gamma):
        """Function to find the true airspeed time derivative (m/s)

        v:          true airspeed in m/s
        m:          mass (kg)
        h:          altitude (m)
        T:          Thrust (N)
        gamma:      flight path angle (deg)

        """

        D = drag.clean(m, v / aero.kts, h / aero.ft, gamma)
        vdot = (T - D) / m - aero.g0 * ca.sin(gamma * ca.pi / 180)
        return vdot

    def dpsi(v, phi, gamma):
        """Function to find the heading angle time derivative

        v:          true airspeed in m/s
        phi:        bank angle (deg)
        gamma:      flight path angle (deg)

        """

        psidot = aero.g0 * ca.tan(phi * ca.pi / 180) / (v * ca.cos(gamma * ca.pi / 180))
        return psidot

    def dm(T, h):
        """Function to find the time derivative of mass (kg)

        T:          Thrust (N)
        h:          altitude (m)
        FFmodel:    Fuel flow model (OpenAP)

        """

        mdot = -fuelflow.at_thrust(acthr=T, alt=h / aero.ft)
        return mdot


# Initialize
AP1_n = "EHAM"  # Departure Airport
AP2_n = "LEMD"  # Arrival Airport
ac = "A320"  # 'A320' 'A321' 'A388' 'B77w' 'B788' 'B789', 'B744', B738

# Fly from airport to airport. If 'False', fly between coordinates
fly_apt = False

# Direct collocation set-up
N = 20  # No. Control Intervals
poly_degree = 5  # Degree of the interpolating polynomial
fixed_alt = True  # Set altitude fix
fixed_M = False  # Set Mach fix

aircraft = prop.aircraft(ac)
engine = prop.engine(aircraft["engine"]["default"])
drag = Drag(ac, wave_drag=False)
fuelflow = FuelFlow(ac, aircraft["engine"]["default"])
wrap = WRAP(ac)


# Lower bound initial conditions for x
xp_0lb = 0
yp_0lb = 0
h_0lb = 2000 if fixed_alt else 9000
m_0lb = aircraft["limits"]["MTOW"] - 10000
M_0lb = 0.775 if fixed_M else wrap.cruise_mach()["minimum"]
x_0lb = [xp_0lb, yp_0lb, h_0lb, 0, m_0lb]

# Upper bound initial conditions for x
xp_0ub = xp_0lb
yp_0ub = yp_0lb
h_0ub = (
    aircraft["limits"]["ceiling"] if fixed_alt else h_0lb
)  #   aircraft['limits']['ceiling']
m_0ub = m_0lb
M_0ub = 0.785 if fixed_M else wrap.cruise_mach()["maximum"]
x_0ub = [xp_0ub, yp_0ub, h_0ub, ca.inf, m_0ub]

# Lower bound final conditions for x
xp_flb = 0
yp_flb = 400000
h_flb = h_0lb
m_flb = aircraft["limits"]["OEW"]
M_flb = M_0lb
x_flb = [xp_flb, yp_flb, h_flb, 0, m_flb]

# upper bound final conditions for x
xp_fub = xp_flb
yp_fub = yp_flb
h_fub = h_0ub
m_fub = ca.inf
M_fub = M_0ub
x_fub = [xp_fub, yp_fub, h_fub, ca.inf, m_fub]

# Lower bound x
xp_lb = min(xp_0lb, xp_flb) - 10000
yp_lb = min(yp_0lb, yp_flb) - 10000
h_lb = 2000
m_lb = aircraft["limits"]["OEW"]
M_lb = M_0lb
x_lb = [xp_lb, yp_lb, h_lb, 0, m_lb]

# Upper bound x
xp_ub = max(xp_0ub, xp_fub) + 10000
yp_ub = max(yp_0ub, yp_fub) + 10000
h_ub = aircraft["limits"]["ceiling"]
m_ub = aircraft["limits"]["MTOW"]
M_ub = M_0ub
x_ub = [xp_ub, yp_ub, h_ub, ca.inf, m_ub]

# Initial guess x
xp_g = np.linspace(0, xp_fub, N + 1)
yp_g = np.linspace(0, yp_fub, N + 1)
h_g = [h_ub] * (N + 1)
v_g = [aero.mach2tas(wrap.cruise_mach()["maximum"], np.mean(h_g))] * (N + 1)
m_g = [m_ub] * (N + 1)
x_guess = [[xp_g[i], yp_g[i], h_g[i], v_g[i], m_g[i]] for i in range(N + 1)]

# x_guess = [xp_g, yp_g, h_g, v_g, m_g]

# Lower bound u
T_lb = 0 if np.isnan(engine["cruise_thrust"]) else engine["cruise_thrust"] * 1
gamma_lb = -0.00001 if fixed_alt else -10  # deg
psi_lb = -ca.inf  # deg
phi_lb = -30  # deg
u_lb = [T_lb, gamma_lb, psi_lb]

# Upper bound u
T_ub = engine["max_thrust"] * aircraft["engine"]["number"]
gamma_ub = -gamma_lb  # deg
psi_ub = ca.inf  # deg
phi_ub = -phi_lb  # deg
u_ub = [T_ub, gamma_ub, psi_ub]

# Initial guess u
T_g = T_lb * 2
gamma_g = 0
psi_g = 0
phi_g = 0
u_guess = [T_g, gamma_g, psi_g]


params_u, params_v = 0, 0
df = 0  # Set to 0 for plotting

# =============================================================================
# Pre-collocation setup
# =============================================================================

tau_root = np.append(
    0, ca.collocation_points(poly_degree, "legendre")
)  # Get collocation points
C = np.zeros(
    (poly_degree + 1, poly_degree + 1)
)  # Coefficients of the collocation equation
D = np.zeros(poly_degree + 1)  # Coefficients of the continuity equation
B = np.zeros(poly_degree + 1)  # Coefficients of the quadrature function

# Construct polynomial basis
for j in range(poly_degree + 1):
    # Construct Lagrange polynomials to get the polynomial basis at the collocation point
    p = np.poly1d([1])
    for r in range(poly_degree + 1):
        if r != j:
            p *= np.poly1d([1, -tau_root[r]]) / (tau_root[j] - tau_root[r])

    # Evaluate the polynomial at the final time to get the coefficients of the continuity equation
    D[j] = p(1.0)

    # Evaluate the time derivative of the polynomial at all collocation points to get the coefficients of the continuity equation
    pder = np.polyder(p)
    for r in range(poly_degree + 1):
        C[j, r] = pder(tau_root[r])

    # Evaluate the integral of the polynomial to get the coefficients of the quadrature function
    pint = np.polyint(p)
    B[j] = pint(1.0)


# =============================================================================
# Model variables
# =============================================================================

xp = ca.MX.sym("xp")
yp = ca.MX.sym("yp")
h = ca.MX.sym("h")
v = ca.MX.sym("v")
m = ca.MX.sym("m")
x = ca.vertcat(xp, yp, h, v, m)

thrust = ca.MX.sym("thrust")
gamma = ca.MX.sym("gamma")
psi = ca.MX.sym("psi")
u = ca.vertcat(thrust, gamma, psi)

T = 1  # Final time is not known
Tf = ca.MX.sym("Tf")

# Establish dynamic model
xdot = Tf * ca.vertcat(
    EOM.dx(v, psi, gamma, xp, yp, h, params_u),
    EOM.dy(v, psi, gamma, xp, yp, h, params_v),
    EOM.dh(v, gamma),
    EOM.dv(v, m, h, thrust, gamma),
    EOM.dm(thrust, h),
)

# Objective term
L = EOM.dm(thrust, h)

# Continuous time dynamics
f = ca.Function("f", [x, u], [xdot, L], ["x", "u"], ["xdot", "L"])

# Control discretization
dt = T / N

# Start with an empty NLP
w = []  # Containing all the states & controls generated
w0 = []  # Containing the initial guess for w
lbw = []  # Lower bound constraints on the w variable
ubw = []  # Upper bound constraints on the w variable
J = 0  # Objective function value?
g = []  # Constraint function
lbg = []  # Constraint lb value
ubg = []  # Constraint ub value

# For plotting x and u given w
x_plot = []
u_plot = []


# Apply initial conditions
Xk = ca.MX.sym("X0", x.shape[0], x.shape[1])
w.append(Xk)
lbw.append(x_0lb)
ubw.append(x_0ub)
w0.append(x_guess[0])
x_plot.append(Xk)

# Path constraint for max velocity (dependent on alt)
g.append(aero.mach2tas(M_0ub, Xk[2]) - Xk[3])
lbg.append([0])
ubg.append([ca.inf])

# Path constraint for min velocity (dependent on alt)
g.append(aero.mach2tas(M_0lb, Xk[2]) - Xk[3])
lbg.append([-ca.inf])
ubg.append([0])


# Formulate the NLP
for k in range(N):
    # New NLP variable for the control
    Uk = ca.MX.sym("U_" + str(k), u.shape[0])
    w.append(Uk)
    lbw.append(u_lb)
    ubw.append(u_ub)
    w0.append(u_guess)
    u_plot.append(Uk)

    # State at collocation points
    Xc = []
    for j in range(poly_degree):
        Xkj = ca.MX.sym("X_" + str(k) + "_" + str(j), x.shape[0])
        Xc.append(Xkj)
        w.append(Xkj)
        lbw.append(x_lb)
        ubw.append(x_ub)
        w0.append(x_guess[k + 1])

        # Path constraint for max speed (dependent on alt)
        g.append(aero.mach2tas(M_ub, Xk[2]) - Xk[3])
        lbg.append([0])
        ubg.append([ca.inf])

        # Path constraint for min speed (dependent on alt)
        g.append(aero.mach2tas(M_lb, Xk[2]) - Xk[3])
        lbg.append([-ca.inf])
        ubg.append([0])

    # Loop over collocation points
    Xk_end = D[0] * Xk
    for j in range(1, poly_degree + 1):
        # Expression for the state derivative at the collocation point
        xp = C[0, j] * Xk
        for r in range(poly_degree):
            xp = xp + C[r + 1, j] * Xc[r]

        # Append collocation equations
        fj, qj = f(Xc[j - 1], Uk)
        g.append(dt * fj - xp)
        lbg.append([0] * x.shape[0])  # As many constraints as there are controls
        ubg.append([0] * x.shape[0])

        # Add contribution to the end state
        Xk_end = Xk_end + D[j] * Xc[j - 1]

        # Add contribution to quadrature function
        J = J + B[j] * qj * dt

    # New NLP variable for state at end of interval
    Xk = ca.MX.sym("X_" + str(k + 1), x.shape[0])
    w.append(Xk)
    x_plot.append(Xk)

    if k != N - 1:
        lbw.append(x_lb)
        ubw.append(x_ub)
        w0.append(x_guess[k + 1])

        # Path constraint for max speed (dependent on alt)
        g.append(aero.mach2tas(M_ub, Xk[2]) - Xk[3])
        lbg.append([0])
        ubg.append([ca.inf])

        # Path constraint for min speed (dependent on alt)
        g.append(aero.mach2tas(M_lb, Xk[2]) - Xk[3])
        lbg.append([-ca.inf])
        ubg.append([0])

    # Final conditions
    else:
        lbw.append(x_flb)
        ubw.append(x_fub)
        w0.append(x_guess[-1])

        # Path constraint for max speed (dependent on alt)
        g.append(aero.mach2tas(M_fub, Xk[2]) - Xk[3])
        lbg.append([0])
        ubg.append([ca.inf])

        # Path constraint for min speed (dependent on alt)
        g.append(aero.mach2tas(M_flb, Xk[2]) - Xk[3])
        lbg.append([-ca.inf])
        ubg.append([0])

    # Add equality constraint
    g.append(Xk_end - Xk)
    lbg.append([0] * x.shape[0])
    ubg.append([0] * x.shape[0])

w.append(Tf)
lbw.append([0])
ubw.append([100000])
w0.append([14000])  # TODO: Improve initial guess using the distance & velocity


# Concatenate vectors
w = ca.vertcat(*w)
g = ca.vertcat(*g)
x_plot = ca.horzcat(*x_plot)
u_plot = ca.horzcat(*u_plot)
w0 = np.concatenate(w0)
lbw = np.concatenate(lbw)
ubw = np.concatenate(ubw)
lbg = np.concatenate(lbg)
ubg = np.concatenate(ubg)

# Create an NLP solver
options = {"ipopt": {"max_iter": 10000}}
prob = {"f": -Xk_end[4], "x": w, "g": g}
solver = ca.nlpsol("solver", "ipopt", prob, options)

# Function to get x and u trajectories from w
trajectories = ca.Function("trajectories", [w], [x_plot, u_plot], ["w"], ["x", "u"])

# Solve the NLP
sol = solver(x0=w0, lbx=lbw, ubx=ubw, lbg=lbg, ubg=ubg)
x_opt, u_opt = trajectories(sol["x"])
x_opt = x_opt.full()  # to numpy array
u_opt = u_opt.full()  # to numpy array

x_vals, y_vals, h_vals, v_vals, m_vals = x_opt
T_vals, gamma_vals, psi_vals = u_opt
Tf_val = sol["x"][-1].full()[0][0]
tgrid = np.linspace(0, Tf_val, N + 1)
tgrid_u = np.linspace(0, Tf_val, N)

# Average fuel flow per meter travelled
average_ff = (m_vals[0] - m_vals[-1]) / (np.sqrt(x_vals[-1] ** 2 + y_vals[-1] ** 2))

# =============================================================================
# # Plot the result
# =============================================================================
plt.figure("pos")
plt.plot(x_vals, y_vals, label="xypos")
plt.xlabel("xpos (m)")
plt.ylabel("ypos (m)")
plt.ylim(yp_lb, yp_ub)
plt.xlim(xp_lb, xp_ub)
plt.legend()
plt.show()

plt.figure("altitude")
plt.plot(tgrid, h_vals, label="altitude")
plt.xlabel("time (s)")
plt.ylabel("hpos (m)")
plt.ylim(0, h_ub * 1.1)
plt.plot(tgrid_u, [h_ub] * N, "--", label="max h")
plt.plot(tgrid_u, [h_lb] * N, "--", label="min h")
plt.xlim(0, Tf_val)
plt.legend()
plt.show()
