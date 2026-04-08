st = "junction 1 0 [color=yellow gta=5 max_drones=2]"

l = st.split()[3:]
print([p.strip("[]") for p in l])
