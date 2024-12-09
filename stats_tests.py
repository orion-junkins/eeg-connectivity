import numpy as np
import pingouin as pg
import pandas as pd
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests

def run_wilcoxon(condition_1, condition_2):
    p_values = np.ones((12, 12))
    test_stats = np.ones((12, 12))
    median_diffs = np.ones((12, 12))
    
    for i in range(12):
        for j in range(12):
            if i <=j:
                continue

            cur_1 = condition_1[:, i, j]
            cur_2 = condition_2[:, i, j]
            
            stat, p_value = wilcoxon(cur_1, cur_2)

            diffs = cur_1 - cur_2
            median_diff = np.median(diffs)

            p_values[i, j], p_values[j, i] = p_value, p_value
            test_stats[i, j], test_stats[j, i] = stat, stat
            median_diffs[i, j], median_diffs[j, i] = median_diff, median_diff
    
    # Run FDR correction
    mask = np.tril(np.ones(p_values.shape), k=-1).astype(bool)
    p_values_masked = p_values[mask]
    p_values_adj = multipletests(p_values_masked, alpha=0.05, method='fdr_bh')[1]

    p_values = np.ones_like(p_values)
    p_values[mask] = p_values_adj
    
    return p_values, test_stats, median_diffs
            
def run_anova(group_A_condition_1, group_A_condition_2, group_B_condition_1, group_B_condition_2):
    # groups will be n x 12 x 12
    assert(group_A_condition_1.shape == group_A_condition_2.shape)
    assert(group_A_condition_1[0].shape == group_B_condition_1[0].shape)
    assert(group_B_condition_1.shape == group_B_condition_2.shape)

    p_values_group = np.ones_like(group_A_condition_1[0])
    p_values_condition = np.ones_like(group_A_condition_1[0])
    p_values_interaction = np.ones_like(group_A_condition_1[0])

    for i in range(12):
        for j in range(12):
            if i <= j: 
                continue
            
            data = {
                "subject_id": [],
                "group": [],
                "condition": [],
                "plv": []
                }
        
            for idx, subject in enumerate(group_A_condition_1):
                subject_id = idx
                group = "A"
                condition = "1"
            
                plv = subject[i, j]
                data["subject_id"].append(subject_id)
                data["group"].append(group)
                data["condition"].append(condition)
                data["plv"].append(plv)
            
            for idx, subject in enumerate(group_A_condition_2):
                subject_id = idx
                group = "A"
                condition = "2"
            
                plv = subject[i, j]
                data["subject_id"].append(subject_id)
                data["group"].append(group)
                data["condition"].append(condition)
                data["plv"].append(plv)
            
            for idx, subject in enumerate(group_B_condition_1):
                subject_id = idx + len(group_A_condition_1)
                group = "B"
                condition = "1"
            
                plv = subject[i, j]
                data["subject_id"].append(subject_id)
                data["group"].append(group)
                data["condition"].append(condition)
                data["plv"].append(plv)
            
            for idx, subject in enumerate(group_B_condition_2):
                subject_id = idx + len(group_A_condition_1)
                group = "B"
                condition = "2"
            
                plv = subject[i, j]
                data["subject_id"].append(subject_id)
                data["group"].append(group)
                data["condition"].append(condition)
                data["plv"].append(plv)
            
            
            df = pd.DataFrame(data)

            # Anova
            anova_results = pg.mixed_anova(data=df, dv='plv', between='group', within='condition', subject='subject_id', correction=False)
            p_values_group[i, j] = anova_results['p-unc'][0]
            p_values_condition[i, j] = anova_results['p-unc'][1]
            p_values_interaction[i, j] = anova_results['p-unc'][2]
    
    # Extract the p-values from the lower triangular part
    mask = np.tril(np.ones(p_values_group.shape), k=-1).astype(bool)
    p_values_group_masked = p_values_group[mask]
    p_values_condition_masked = p_values_condition[mask]
    p_values_interaction_masked = p_values_interaction[mask]


    # Apply Benjamini-Hochberg FDR correction
    p_values_group_adj = multipletests(p_values_group_masked, alpha=0.05, method='fdr_bh')[1]
    p_values_condition_adj = multipletests(p_values_condition_masked, alpha=0.05, method='fdr_bh')[1]
    p_values_interaction_adj = multipletests(p_values_interaction_masked, alpha=0.05, method='fdr_bh')[1]

    
    p_values_group = np.ones_like(p_values_group)
    p_values_condition = np.ones_like(p_values_group)
    p_values_interaction = np.ones_like(p_values_group)

    p_values_group[mask] = p_values_group_adj
    p_values_condition[mask] = p_values_condition_adj
    p_values_interaction[mask] = p_values_interaction_adj
    return p_values_group, p_values_condition, p_values_interaction