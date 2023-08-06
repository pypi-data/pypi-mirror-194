import os
import datetime

def link_files(paths, old_names, new_names, date_in, date_fin, time_res, out_paths):
    current_date = date_in
    while current_date <= date_fin:
        # Loop through paths
        for path, old_name, new_name, out_path in zip(paths, old_names, new_names, out_paths):
            # Find files
            u_file = None
            v_file = None
            for file in os.listdir(path):
                for i in range(len(old_name)):
                    if old_name[i] in file and time_res[i] in file and current_date.strftime('%Y%m%d') in file:
                        if 'U' in file:
                            u_file = os.path.join(path, file)
                        elif 'V' in file:
                            v_file = os.path.join(path, file)
            
            # Link files to output folder
                if u_file is not None and v_file is not None:
                    os.link(u_file, os.path.join(out_path[i], f"{new_name[i]}_{time_res[i]}_{current_date}_grid_U.nc"))
                    os.link(v_file, os.path.join(out_path[i], f"{new_name[i]}_{time_res[i]}_{current_date}_grid_V.nc"))
                elif u_file is not None and 'U' in u_file:
                    os.link(u_file, os.path.join(out_path[i], f"{new_name[i]}_{time_res[i]}_{current_date}_grid_U.nc"))
                elif v_file is not None and 'V' in v_file:
                    os.link(v_file, os.path.join(out_path[i], f"{new_name[i]}_{time_res[i]}_{current_date}_grid_V.nc"))

        # Increment date
        current_date += datetime.timedelta(days=1)