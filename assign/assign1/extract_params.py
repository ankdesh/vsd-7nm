import re
import sys

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
    if len(sys.argv) < 2:
        print("Usage: python3 extract_params.py <logfile>")
        return

    log_file = sys.argv[1]
    
    try:
        with open(log_file, 'r') as f:
            content = f.read()
            
        data = extract_values(content)
        
        print("Extracted Values:")
        print("-" * 20)
        print(f"Vth: {data.get('Vth', 'Not Found')} V")
        print(f"Id:  {data.get('Id', 'Not Found')} A")
        print(f"P:   {data.get('P', 'Not Found')} W")
        print(f"tpd: {data.get('tpd', 'Not Found')} ps")
        print(f"Av:  {data.get('Av', 'Not Found')}")
        print(f"f:   {data.get('f', 'Not Found')} Hz")
        
    except FileNotFoundError:
        print(f"Error: File {log_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
