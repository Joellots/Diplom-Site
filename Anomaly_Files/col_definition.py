
columns = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count","srv_count","serror_rate", "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate", "diff_srv_rate", "srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","attack", "last_flag"]

numeric_cols = ["duration","src_bytes","dst_bytes",
"wrong_fragment","urgent","hot","num_failed_logins",
"num_compromised","num_root","num_file_creations",
"num_shells","num_access_files","num_outbound_cmds","count","srv_count","serror_rate", "srv_serror_rate",
"rerror_rate","srv_rerror_rate","same_srv_rate", "diff_srv_rate", "srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
"dst_host_diff_srv_rate","dst_host_same_src_port_rate",
"dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
"dst_host_rerror_rate","dst_host_srv_rerror_rate"]

categorical_cols = ["protocol_type", "service", "flag"]

binary_cols = ['land', 'logged_in', 'root_shell', 'su_attempted', 'is_host_login', 'is_guest_login']

target_cols = ['attack']

raw_selected_cols = ['land',
 'wrong_fragment',
 'logged_in',
 'serror_rate',
 'srv_serror_rate',
 'dst_host_same_src_port_rate',
 'dst_host_serror_rate',
 'dst_host_srv_serror_rate',
 'protocol_type',
 'service',
 'flag',
 'dst_host_same_srv_rate',
 'same_srv_rate',
 'dst_host_srv_diff_host_rate',
 'dst_host_srv_count',
 'srv_rerror_rate', 
 'dst_host_srv_rerror_rate',]

attack_class = {
    "DoS" : ['back', 'land', 'neptune', 'pod', 'smurf', 'teardrop', 'apache2', 'udpstorm', 'processtable', 'worm'],
    "Probe" : ['satan', 'ipsweep', 'nmap', 'portsweep', 'mscan', 'saint'],
    "R2L" : ['guess_passwd', 'ftp_write', 'imap', 'phf', 'multihop', 'warezmaster', 'warezclient', 'spy', 'xlock', 'xsnoop', 'snmpguess', 'snmpgetattack', 'httptunnel', 'sendmail', 'named'],
    "U2R" : ['buffer_overflow', 'loadmodule', 'rootkit', 'perl', 'sqlattack', 'xterm', 'ps',]
}

my_attack = ['neptune','normal','smurf','ipsweep','back','nmap','warezclient','satan', 'portsweep', 'teardrop', 'guess_passwd', 'pod', 'rootkit', 'ftp_write', 'buffer_overflow', 'land', 'multihop', 'imap', 'loadmodule', 'perl', 'warezmaster', 'phf', 'spy']

feature_map = {
    'duration': 'DURATION',
    'protocol_type': 'PROTOCOL TYPE (protocol_type)',
    'service': 'SERVICE (service)',
    'flag': 'FLAG (flag)',
    'src_bytes': 'SOURCE BYTES',
    'dst_bytes': 'DESTINATION BYTES',
    'dst_host_same_src_port_rate': 'DESTINATION HOST SAME SERVICE PORT RATE',
    'srv_count': 'SAME SERVICE COUNT',
    'dst_host_rerror_rate' : 'DESTINATION HOST R-FLAG ERROR RATE',
    
    'dst_host_same_srv_rate': 'DESTINATION HOST SAME SERVICE RATE',
    'dst_host_diff_srv_rate': 'DESTINATION HOST DIFFERENT SERVICE RATE',
    'dst_host_srv_rerror_rate': 'DESTINATION HOST SERVICE R-FLAG ERROR RATE',
    'same_srv_rate': 'SAME SERVICE RATE',
    
    'dst_host_srv_count': 'DESTINATION HOST SAME SERVICE COUNT',
    'diff_srv_rate': 'DIFFERENT SERVICE RATE',
    'count': 'COUNT',
    'dst_host_srv_diff_host_rate': 'DESTINATION HOST SERVICE RATE FROM DIFFERENT HOST',
    'dst_host_srv_serror_rate': 'DESTINATION HOST SERVICE S-FLAG ERROR RATE',
    'dst_host_serror_rate': 'DESTINATION HOST S-FLAG ERROR RATE'
    

}



#############################################################################################################

# 'land': 'LAND',
# 'wrong_fragment': 'WRONG FRAGMENT',
# 'logged_in': 'LOGGED IN',
# 'serror_rate': 'S-ERROR RATE',
# 'srv_serror_rate': 'SERVICE S-FLAG ERROR RATE',
# 'dst_host_serror_rate' : 'DESTINATION HOST S-FLAG ERROR RATE',
# 'dst_host_srv_serror_rate': 'DESTINATION HOST SERVICE S-FLAG ERROR RATE',
# 'dst_host_srv_diff_host_rate': 'DIFFERENT DESTINATION HOST SERVICE RATE',
# 'srv_rerror_rate': 'SERVICE R-FLAG ERROR RATE', 
    


# Load the joblib file containing the model, scaler, and encoder
# model_info = joblib.load("Anomaly_Forest_Subset")

# #forest = model_info['model']
# # scaler = model_info['scaler']
# # encoder = model_info['encoder']
# # train_inputs_ravel = model_info['train_inputs_ravel']
# # train_inputs_ravel_subset = model_info['train_inputs_ravel_subset']
# # train_targets_ravel = model_info['train_targets_ravel']
# # input_cols = model_info['input_cols']
# # numeric_cols = model_info['numeric_cols']
# categorical_cols = model_info['categorical_cols']
# # #encoded_cols = model_info['encoded_cols']
# selected_cols = model_info['selected_cols']

# def display_all_inputs():
#     for col in selected_cols:
#         if col in numeric_cols:
#             # If the column is binary, present it as a select box with options "0" and "1"
#             if df[col].nunique() == 2:
#                 user_input[col] = st.sidebar.selectbox(col, [0, 1])
#             else:
#                 # Use text_input and handle invalid input for other numeric columns
#                 # user_input[col] = st.sidebar.text_input(col, f"Enter {col}", key=col)
#                 user_input[col] = st.sidebar.text_input(col, f"", key=col)
#                 try:
#                     user_input[col] = float(user_input[col])  # Try to convert to float
#                 except ValueError:
#                     user_input[col] = df[col].mean()  # Default to mean if input is not a valid number

#     for col in selected_cols:
#         if col in categorical_cols:
#             user_input[col] = st.sidebar.selectbox(col, df[col].unique())

##################################################################################################################