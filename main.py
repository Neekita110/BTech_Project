import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load pre-trained models
comp_rate_model = joblib.load('C:/Users/hp/BTP/Models/Comprate_IA26AP+OPERA_xgb.pkl')
dg_model = joblib.load('C:/Users/hp/BTP/Models/dG_IIRA25+OPERA_xgb.pkl')

# Load the full dataset with all features (109 or 359 depending on the model)
data = pd.read_csv('C:/Users/hp/BTP/Data/IA26AP+OPERA_screen.csv')

# Drop non-numeric columns (like SMILES strings) to prevent errors
data_numeric = data.select_dtypes(include=[np.number])

# Streamlit app interface
st.title("CO2 Absorption and Gibbs Free Energy Prediction for BTP IIT Delhi")

# Create two columns: options on the left and prediction results on the right
col1, col2 = st.columns(2)

with col1:
    # Let the user choose between manual input or selecting from dataset
    option = st.radio("Choose how you'd like to provide input:", ('Manual Input', 'Select from Dataset'))

    if option == 'Manual Input':
        # Input fields for molecular descriptors
        mol_weight = st.number_input('Molecular Weight', min_value=50.0, max_value=500.0, value=100.0)
        topo_pol_surf_air = st.number_input('Topological Polar Surface Area', min_value=0.0, max_value=200.0, value=50.0)
        logP_pred = st.number_input('LogP_pred', min_value=-5.0, max_value=5.0, value=0.0)
        nb_atoms = st.number_input('Number of Atoms', min_value=1, max_value=100, value=20)
        nb_heavy_atoms = st.number_input('Number of Heavy Atoms', min_value=1, max_value=50, value=10)

        # Create a full set of 359 features for the dg_model, filling missing values with 0
        input_data = np.zeros((1, 359))  # Initialize a zero array with 359 features
        input_data[0, 0] = mol_weight
        input_data[0, 1] = topo_pol_surf_air
        input_data[0, 2] = logP_pred
        input_data[0, 3] = nb_atoms
        input_data[0, 4] = nb_heavy_atoms

    elif option == 'Select from Dataset':
        # Let the user select a compound from the dataset
        selected_compound = st.selectbox('Select a compound:', data_numeric.index)

        # Extract the feature set for the selected compound (excluding target variables)
        X = data_numeric.drop(['CompRate_ylog', 'dG_MD_ylog'], axis=1, errors='ignore')
        input_data = np.zeros((1, 359))  # Initialize a zero array with 359 features
        selected_features = X.loc[selected_compound].values

        # Fill the first 109 features with the selected compound's data
        input_data[0, :len(selected_features)] = selected_features

        # Show the selected features (optional)
        st.write(f"Selected features for prediction: {input_data}")

with col2:
    # Prediction button
    if st.button('Predict'):
        # Make predictions using the comp_rate_model (only 109 features required)
        comp_rate_prediction = comp_rate_model.predict(input_data[:, :109])

        # Make predictions using the dg_model (359 features required)
        dg_prediction = dg_model.predict(input_data)

        # Display the predictions
        st.success(f'Predicted CO2 Absorption Rate (log scale): {comp_rate_prediction[0]:.4f}')
        st.success(f'Predicted Gibbs Free Energy (ΔG): {dg_prediction[0]:.4f}')
