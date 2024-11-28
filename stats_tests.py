import numpy as np
import pingouin as pg
import pandas as pd
from statsmodels.stats.multitest import multipletests

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
            # if i == 11 and j == 6:
            #     return df

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



def run_anova2(dataset):
    p_values_group = np.ones((12,12))
    p_values_condition = np.ones((12,12))
    p_values_interaction = np.ones((12,12))

    for i in range(12):
        for j in range(12):
            if i <= j: 
                continue

            expert_BL_WiG = dataset.get_frequency_average_for_electrode_pair("expert", "BL", "WiG", "delta", i, j)
            expert_BL_NoG = dataset.get_frequency_average_for_electrode_pair("expert", "BL", "NoG", "delta", i, j)
            novice_BL_WiG = dataset.get_frequency_average_for_electrode_pair("novice", "BL", "WiG", "delta", i, j)
            novice_BL_NoG = dataset.get_frequency_average_for_electrode_pair("novice", "BL", "NoG", "delta", i, j)
            
            data = {
                "subject_id": [],
                "group": [],
                "condition": [],
                "plv": []
                }

            for idx, subject in enumerate(expert_BL_WiG):
                subject_id = idx
                group = "expert"
                condition = "WiG"
                plv = subject
                data["subject_id"].append(subject_id)
                data["group"].append(group)
                data["condition"].append(condition)
                data["plv"].append(plv)
            
            for idx, subject in enumerate(expert_BL_NoG):
                subject_id = idx
                group = "expert"
                condition = "NoG"
                plv = subject
                data["subject_id"].append(subject_id)
                data["group"].append(group)
                data["condition"].append(condition)
                data["plv"].append(plv)
            
            for idx, subject in enumerate(novice_BL_WiG):
                subject_id = idx + len(expert_BL_WiG)
                group = "novice"
                condition = "WiG"
                plv = subject
                data["subject_id"].append(subject_id)
                data["group"].append(group)
                data["condition"].append(condition)
                data["plv"].append(plv)
            
            for idx, subject in enumerate(novice_BL_NoG):
                subject_id = idx + len(expert_BL_WiG)
                group = "novice"
                condition = "NoG"
                plv = subject
                data["subject_id"].append(subject_id)
                data["group"].append(group)
                data["condition"].append(condition)
                data["plv"].append(plv)
            
            df = pd.DataFrame(data)
            if i == 6 and j == 11:
                return df

            # Anova
            anova_results = pg.mixed_anova(data=df, dv='plv', between='group', within='condition', subject='subject_id', correction=False)
            print(i)
            print(j)
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
