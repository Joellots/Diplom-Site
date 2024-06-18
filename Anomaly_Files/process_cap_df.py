import pandas as pd

def compute_metrics(df):
    clean_df = pd.DataFrame()

    # Calculate metrics specific to each packet
    clean_df['dst_host_srv_count'] = df.apply(lambda x: compute_dst_host_srv_count(df, x), axis=1)
    clean_df['dst_host_same_srv_rate'] = df.apply(lambda x: compute_dst_host_same_srv_rate(df, x), axis=1)
    clean_df['dst_host_srv_diff_host_rate'] = df.apply(lambda x: compute_dst_host_srv_diff_host_rate(df, x), axis=1)
    clean_df['dst_host_srv_serror_rate'] = df.apply(lambda x: compute_dst_host_srv_serror_rate(df, x), axis=1)
    clean_df['count'] = df.apply(lambda x: compute_count(df, x), axis=1)
    clean_df['diff_srv_rate'] = df.apply(lambda x: compute_diff_srv_rate(df, x), axis=1)
    clean_df['dst_host_serror_rate'] = df.apply(lambda x: compute_dst_host_serror_rate(df, x), axis=1)
    clean_df['same_srv_rate'] = df.apply(lambda x: compute_same_srv_rate(df, x), axis=1)
    clean_df['dst_host_diff_srv_rate'] = df.apply(lambda x: compute_dst_host_diff_srv_rate(df, x), axis=1)
    clean_df['src_bytes'] = df['ip.len']
    clean_df['dst_bytes'] = df['tcp.urgent_pointer']
    clean_df['dst_host_rerror_rate'] = df.apply(lambda x: compute_dst_host_rerror_rate(df, x), axis=1)
    clean_df['flag'] = df['tcp.flags.mapped']
    
    # Write to CSV for reference
    #clean_df.to_csv('OUTPUT.csv', index=False)
    
    return clean_df

# Helper functions for metrics calculation

def compute_dst_host_srv_count(df, row):
    dst_host_srv_count = df[df['tcp.dstport'] == row['tcp.dstport']]['tcp.srcport'].nunique()
    return dst_host_srv_count

def compute_dst_host_same_srv_rate(df, row):
    group = df[df['ip.dst'] == row['ip.dst']]
    dst_host_count = len(group)
    if dst_host_count == 0:
        return 0.0
    
    max_same_srv_count = group[group['tcp.dstport'] == row['tcp.dstport']].shape[0]
    dst_host_same_srv_rate = max_same_srv_count / dst_host_count
    return dst_host_same_srv_rate

def compute_dst_host_srv_diff_host_rate(df, row):
    group = df[df['tcp.dstport'] == row['tcp.dstport']]
    dst_host_srv_count = len(group)
    if dst_host_srv_count == 0:
        return 0.0
    
    unique_dst_ips = group['ip.dst'].nunique()
    dst_host_srv_diff_host_rate = (dst_host_srv_count - unique_dst_ips) / dst_host_srv_count
    return dst_host_srv_diff_host_rate

def compute_dst_host_srv_serror_rate(df, row):
    total_connections = len(df)
    if total_connections == 0:
        return 0.0
    
    serror_count = df['tcp.flags.mapped'].isin(['S0', 'S1', 'S2', 'S3']).sum()
    dst_host_srv_serror_rate = serror_count / total_connections
    return dst_host_srv_serror_rate

def compute_count(df, row):
    df_sorted = df[df['frame.time_relative'] <= row['frame.time_relative']]
    count = 0
    current_time = row['frame.time_relative']
    current_dst_host = row['ip.dst']
    
    for j, prev_row in df_sorted.iterrows():
        prev_time = prev_row['frame.time_relative']
        prev_dst_host = prev_row['ip.dst']
        
        if current_time - prev_time > 2.0:
            break
        
        if current_dst_host == prev_dst_host:
            count += 1
            
    return count

def compute_diff_srv_rate(df, row):
    total_connections = len(df)
    if total_connections == 0:
        return 0.0
    
    unique_services = df['tcp.dstport'].nunique()
    diff_srv_count = total_connections - unique_services
    diff_srv_rate = diff_srv_count / total_connections
    return diff_srv_rate

def compute_dst_host_serror_rate(df, row):
    group = df[df['ip.dst'] == row['ip.dst']]
    total_connections = len(group)
    if total_connections == 0:
        return 0.0
    
    serror_count = (group['tcp.flags.mapped'].isin(['S0', 'S1', 'S2', 'S3'])).sum()
    dst_host_serror_rate = serror_count / total_connections
    return dst_host_serror_rate

def compute_same_srv_rate(df, row):
    total_connections = len(df)
    if total_connections == 0:
        return 0.0
    
    same_srv_count = df[df['tcp.dstport'] == row['tcp.dstport']].shape[0]
    same_srv_rate = same_srv_count / total_connections
    return same_srv_rate

def compute_dst_host_diff_srv_rate(df, row):
    group = df[df['ip.dst'] == row['ip.dst']]
    total_connections = len(group)
    if total_connections == 0:
        return 0.0
    
    unique_services = group['tcp.dstport'].nunique()
    diff_srv_rate = (total_connections - unique_services) / total_connections
    return diff_srv_rate

def compute_dst_host_rerror_rate(df, row):
    group = df[df['ip.dst'] == row['ip.dst']]
    total_connections = len(group)
    if total_connections == 0:
        return 0.0
    
    rerror_count = (group['tcp.flags.mapped'] == 'REJ').sum()
    rerror_rate = rerror_count / total_connections
    return rerror_rate
