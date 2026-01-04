import os
import subprocess
import shutil
import re

# Import the extraction logic from the previously created key script
# Assuming extract_params.py is in the parent directory or same directory.
# For simplicity, I'll redefine the extraction function here or import it if I can set the path correctly.
# Given the user's environment, I'll just include the function here to be self-contained.

def extract_values(log_content):
    values = {}
    
    # Regex patterns
    # Vth (v_th)
    vth_match = re.search(r"\bv_th\s*=\s*([-\d\.eE+]+)", log_content)
    if vth_match:
        values['Vth'] = float(vth_match.group(1))
        
    # Av (max_gain)
    av_match = re.search(r"\bmax_gain\s*=\s*([-\d\.eE+]+)", log_content)
    if av_match:
        values['Av'] = float(av_match.group(1))
        
    # Id (v2#branch) - checking Initial Transient Solution table
    # Look for v2#branch followed by spaces and a number
    id_match = re.search(r"v2#branch\s+([-\d\.eE+]+)", log_content)
    if id_match:
        values['Id'] = float(id_match.group(1))
        
    # P (power)
    p_match = re.search(r"\bpower\s*=\s*([-\d\.eE+]+)", log_content)
    if p_match:
        values['P'] = float(p_match.group(1))
        
    # tpd (tp)
    tpd_match = re.search(r"\btp\s*=\s*([-\d\.eE+]+)", log_content)
    if tpd_match:
        # Convert seconds to ps (picoseconds) as requested (tpd (ps))
        values['tpd'] = float(tpd_match.group(1)) * 1e12
        
    # f (f)
    f_match = re.search(r"\bf\s*=\s*([-\d\.eE+]+)", log_content)
    if f_match:
        values['f'] = float(f_match.group(1))
        
    return values

def main():
    # Configuration
    template_file = "iterate_params/inverter_finfet_template.spice"
    output_dir = "iterate_params/generated_spice"
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Parameter ranges
    # Parameter ranges
    # Example: nfin values from 10 to 18
    nfet_nfin_values = list(range(10, 19))
    pfet_nfin_values = list(range(10, 19))
    
    results = []
    
    # Read template
    with open(template_file, 'r') as f:
        template_content = f.read()
        
    for n_val in nfet_nfin_values:
        for p_val in pfet_nfin_values:
            # Define parameters for this iteration
            params = {
                "pfet_nfin": str(p_val),
                "nfet_nfin": str(n_val)
            }
            
            # Create file content
            content = template_content
            for key, value in params.items():
                content = content.replace(f"{{{{{key}}}}}", value)
                
            # Filename
            filename = f"inverter_nf_nfin_{n_val}_pf_nfin_{p_val}.spice"
            filepath = os.path.join(output_dir, filename)
            
            # Write spice file
            with open(filepath, 'w') as f:
                f.write(content)
                
            print(f"Generated {filepath}")
            
            # Run simulation
            # Using ngspice in batch mode (-b) and redirecting output
            log_file = filepath + ".log"
            cmd = ["ngspice", "-b", "-r", filepath + ".raw", "-o", log_file, filepath]
            
            print(f"Running simulation for {filename}...")
            try:
                # Running simulation
                subprocess.run(cmd, check=True)
                
                # Extract parameters
                if os.path.exists(log_file):
                    with open(log_file, 'r') as log:
                        log_data = log.read()
                        extracted = extract_values(log_data)
                        extracted['Nfin_nfet'] = n_val
                        extracted['Nfin_pfet'] = p_val
                        results.append(extracted)
                        print(f"Extracted: {extracted}")
                else:
                    print(f"Error: Log file {log_file} not generated.")
                    
            except subprocess.CalledProcessError as e:
                print(f"Error running ngspice for {filename}: {e}")
            
    # Print Summary
    print("\nSummary of Results:")
    print("-" * 130)  # Increased separator length to accommodate new columns
    print(f"{'Nfin_nfet':<12} {'Nfin_pfet':<12} {'(W/L)_nfet':<12} {'(W/L)_pfet':<12} {'Vth (V)':<10} {'Id (A)':<15} {'P (W)':<15} {'tpd (ps)':<15} {'Av':<10} {'f (Hz)':<15}")
    print("-" * 130)
    
    for res in results:
        l_n_val = f"{res.get('Nfin_nfet', 0)}"
        l_p_val = f"{res.get('Nfin_pfet', 0)}"
        
        # Calculate W/L ratios
        # W = Nfin, L = 7 (fixed)
        wl_nfet = float(res.get('Nfin_nfet', 0)) / 7.0
        wl_pfet = float(res.get('Nfin_pfet', 0)) / 7.0
        
        wl_n_str = f"{wl_nfet:.2f}"
        wl_p_str = f"{wl_pfet:.2f}"
        
        vth = f"{res.get('Vth', 0):.4f}"
        id_val = f"{res.get('Id', 0):.4e}"
        p_val = f"{res.get('P', 0):.4e}"
        tpd = f"{res.get('tpd', 0):.4f}"
        av = f"{res.get('Av', 0):.4f}"
        f_val = f"{res.get('f', 0):.4e}"
        
        print(f"{l_n_val:<12} {l_p_val:<12} {wl_n_str:<12} {wl_p_str:<12} {vth:<10} {id_val:<15} {p_val:<15} {tpd:<15} {av:<10} {f_val:<15}")

if __name__ == "__main__":
    main()
