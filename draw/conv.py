import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Data extraction from output files
grid_levels = ['Coarse (2 elements)', 'Medium (8 elements)', 'Fine (32 elements)']
h_values = np.array([2.0, 1.0, 0.5])  # Characteristic mesh size
numerical_displacement = np.array([8.24, 16.51, 28.20])  # Numerical solution (mm)
theoretical_displacement = 32.0  # Theoretical solution (mm)

# Calculate L2 norm errors
l2_errors = np.abs(numerical_displacement - theoretical_displacement)
relative_errors = l2_errors / theoretical_displacement * 100

# Calculate convergence rate
log_h = np.log(h_values)
log_error = np.log(l2_errors)
slope, intercept, r_value, p_value, std_err = stats.linregress(log_h, log_error)
overall_rate = slope

# Create log-log plot
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

# Plot numerical results
ax.loglog(h_values, l2_errors, 'bo-', linewidth=3, markersize=10, 
          label='Numerical Results', markerfacecolor='blue', markeredgecolor='darkblue')

# Fitting line
h_fit = np.logspace(np.log10(0.4), np.log10(2.2), 100)
error_fit = np.exp(intercept) * h_fit**overall_rate
ax.loglog(h_fit, error_fit, 'r--', linewidth=2, 
           label=f'Fitted Line: $||e||_{{L2}} = {np.exp(intercept):.2f} \\times h^{{{overall_rate:.2f}}}$')

# Theoretical convergence rate reference line (p=2)
error_theory = l2_errors[1] * (h_fit/h_values[1])**2
ax.loglog(h_fit, error_theory, 'g:', linewidth=2, alpha=0.8, 
           label='Theoretical Rate: $p = 2$')

# Set axes labels and title
ax.set_xlabel('Characteristic Mesh Size h', fontsize=14)
ax.set_ylabel('L2 Norm Error (mm)', fontsize=14)
ax.set_title('T3 Element Convergence Analysis: L2 Error vs Mesh Size\n(Log-Log Scale)', 
             fontsize=16, fontweight='bold', pad=20)

# Grid and legend
ax.grid(True, alpha=0.3, which='both')
ax.legend(fontsize=12, loc='upper left')

# Add data point annotations
for i, (h, error) in enumerate(zip(h_values, l2_errors)):
    ax.annotate(f'h={h:.1f}\n$||e||_{{L2}}$={error:.2f}mm', 
                xy=(h, error), xytext=(15, 15), 
                textcoords='offset points', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.8),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

# Add convergence rate information text box
textstr = f'Convergence Analysis:\nActual Rate: p = {overall_rate:.3f}\nTheoretical Rate: p = 2.0\nR-squared: R² = {r_value**2:.6f}'
props = dict(boxstyle='round', facecolor='lightblue', alpha=0.8)
# ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
#         verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('convergence_analysis.png', dpi=300, bbox_inches='tight')
print("Figure saved as 'convergence_analysis.png'")

print("="*70)
print("T3 Element Convergence Analysis Results")
print("="*70)
print(f"Actual Convergence Rate: p = {overall_rate:.3f}")
print(f"Theoretical Convergence Rate: p = 2.0")
print(f"Convergence Rate Deviation: {abs(overall_rate - 2.0):.3f}")
print(f"R-squared: R² = {r_value**2:.6f}")
print("\nConvergence Verification: PASSED" if abs(overall_rate - 2.0) < 0.5 else "\nConvergence Verification: FAILED")

# Print detailed data table
print("\n" + "="*80)
print("Detailed Convergence Data")
print("="*80)
print(f"{'Grid Level':<15} {'h Value':<10} {'Displacement':<15} {'L2 Error':<12} {'Relative Error':<15}")
print(f"{'':^15} {'':^10} {'(mm)':<15} {'(mm)':<12} {'(%)':<15}")
print("-"*80)
for i, level in enumerate(grid_levels):
    print(f"{level:<15} {h_values[i]:<10.1f} {numerical_displacement[i]:<15.2f} {l2_errors[i]:<12.2f} {relative_errors[i]:<15.2f}")
print(f"{'Theoretical':<15} {'0':<10} {theoretical_displacement:<15.1f} {'0':<12} {'0':<15}")

# Calculate error reduction factors
print("\nError Reduction Analysis:")
for i in range(1, len(l2_errors)):
    reduction_factor = l2_errors[i-1] / l2_errors[i]
    print(f"{grid_levels[i-1]} → {grid_levels[i]}: {reduction_factor:.2f}x improvement")