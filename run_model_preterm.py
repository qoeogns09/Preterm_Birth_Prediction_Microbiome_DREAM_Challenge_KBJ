from joblib import load
import argparse
import pandas as pd
import os
import numpy as np

def sv_to_num(sv):
    try:
        num = int(sv.split('___')[1])
    except:
        num = None
    return num

def sv_for_features(df, index, cols):
    df['num_sv'] = df.sv.map(lambda x: sv_to_num(x))
    
    num_features = 53129
   
    features = []
    for specimen in index:
        feature = np.zeros(num_features)
        new_df = df[df['specimen'] == specimen]
        sv = np.array(new_df['num_sv'])
        fract = np.array(new_df['fract'])
        for i in range(len(sv)):
            if sv[i] == None:
                continue
            else:
                feature[sv[i]-1] = fract[i]
        features.append(feature)
    df_features = pd.DataFrame(features, index=index, columns = cols)
    df_features.index.name = 'specimen'
    return df_features

def merge_df(A):
    df = A[0]
    for i in range(1, len(A)):
        df = pd.merge(df, A[i], on='specimen')
    return df

def main():
    parser = argparse.ArgumentParser(description='Run the model on test data')
    parser.add_argument(
        '--input', '-I',
        help='Directory with the data',
        default='/input'
    )
    parser.add_argument(
        '--output', '-O',
        help='Where to place the CSV file with per-participant predictions',
        default='/output'
    )
    parser.add_argument(
        '--preterm_model', '-m_pt',
        help='Model to predict preterm by specimen',
        default='/model_code/preterm.save'
    )
    parser.add_argument(
        '--early_preterm_model', '-m_ept',
        help='Model to predict early preterm by specimen',
        default='/model_code/early_preterm.save'
    )
    parser.add_argument(
        '--task', '-T',
        choices=(
            'preterm',
            'early_preterm'
        ),
        default='preterm',
        help='Which Task? preterm or early_preterm'
    )
    args = parser.parse_args()

    eclf1 = load('/model_code/model_1.save')
    eclf2 = load('/model_code/model_2.save')
    eclf3 = load('/model_code/model_3.save')
    eclf4 = load('/model_code/model_4.save')
    eclf5 = load('/model_code/model_5.save')
        
    metadata = pd.read_csv(
        os.path.join(args.input, 'metadata', 'metadata.csv')
    )
    
    tax_genus = pd.read_csv(
        os.path.join(args.input, 'taxonomy', 'taxonomy_relabd.genus.csv'),
    )

    pt_ra_1e_1 = pd.read_csv(
        os.path.join(args.input, 'phylotypes', 'phylotype_relabd.1e_1.csv'),
    )

    alpha = pd.read_csv(
        os.path.join(args.input, 'alpha_diversity', 'alpha_diversity.csv'),
    )

    cst = pd.read_csv(
        os.path.join(args.input, 'community_state_types', 'cst_valencia.csv'),
    )
    sv_counts = pd.read_csv(
        os.path.join(args.input, 'sv_counts', 'sp_sv_long.csv'),
    )
    race_meta = pd.read_csv(
        os.path.join(args.input, 'metadata', 'metadata_normalized.csv')
    )
    
    specimen_participant = {
        sp: p
        for (sp, p) in zip(
            metadata.specimen,
            metadata.participant_id
        )
    }
    index = np.array(metadata.specimen)
    cols = np.load('sv_cols.npy')
    new_sv = sv_for_features(sv_counts, index, cols)
    
    selected_features = np.load('use_features.npy')

    # input df
    meta = metadata[['specimen', 'participant_id']]
    race_meta = race_meta[['Race: American Indian or Alaska Native', 'Race: Asian',
                           'Race: Black or African American',
                           'Race: Native Hawaiian or Other Pacific Islander', 'Race: Unknown',
                           'Race: White', 'specimen']]


    df = merge_df([meta, tax_genus, pt_ra_1e_1, alpha, cst, new_sv, race_meta])
    df = df.drop(columns = ['CST', 'subCST', 'specimen'])

    dup = df.duplicated('participant_id', keep=False)
    duplicated = df[dup]
    dup_mean = duplicated.groupby(['participant_id'], as_index=False).aggregate(np.mean)
    df = df.drop_duplicates(['participant_id'], keep=False)
    df = pd.concat([df, dup_mean])
    df = df.set_index('participant_id')
    
    test_X = np.array(df[selected_features])
    
    eclf1_pred_ = eclf1.predict_proba(test_X)
    eclf2_pred_ = eclf2.predict_proba(test_X)
    eclf3_pred_ = eclf3.predict_proba(test_X)
    eclf4_pred_ = eclf4.predict_proba(test_X)
    eclf5_pred_ = eclf5.predict_proba(test_X)

    
    preds = (eclf1_pred_ + eclf2_pred_ + eclf3_pred_ + eclf4_pred_ + eclf5_pred_)/5.0
    label = np.argmax(preds, axis=1).reshape(-1)
    
    predicts = pd.DataFrame(np.array(df.index), columns=[f'participant'])
    predicts[f'was_{args.task}'] = label
    predicts['probability'] = preds[:,1]
    predicts = predicts.sort_values(by=["participant"], ascending=[True]) 
    predicts.to_csv(
        os.path.join(args.output, 'predictions.csv'),
        index=None
    )


if __name__ == "__main__":
    main()
