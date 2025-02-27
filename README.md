# Rock Mass Rating (RMR) Calculator

## Description

This Streamlit web application calculates the Rock Mass Rating (RMR) based on Bieniawski's classification system and determines appropriate roof bolt support requirements for mining and tunneling operations. The application provides an interactive interface for engineers, geologists, and mining professionals to perform RMR calculations, visualize support patterns, and get detailed support recommendations.

## Features

- Interactive calculation of RMR based on five key parameters:
  - Uniaxial Compressive Strength (UCS)
  - Rock Quality Designation (RQD)
  - Spacing of Discontinuities
  - Condition of Discontinuities
  - Groundwater Conditions
- Automatic determination of rock mass class and description
- Comprehensive roof bolt support recommendations, including:
  - Bolt length and spacing
  - Support pattern
  - Bolt type and capacity requirements
  - Additional support measures
- Visual representation of the bolt pattern for the excavation
- Estimation of total bolts required for the project
- Educational information about RMR and its applications

## Installation

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/rmr-calculator.git
   cd rmr-calculator
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

5. The app will open in your default web browser at `http://localhost:8501`

### Deployment on GitHub Pages

To deploy this app on GitHub Pages, you can use [Streamlit Sharing](https://streamlit.io/sharing) or [Streamlit Cloud](https://streamlit.io/cloud) which are free services for deploying Streamlit apps.

Alternatively, if you want to use GitHub Pages directly:

1. Create a new GitHub repository
2. Push your code to the repository
3. Go to Settings > Pages
4. Select the main branch as the source
5. Click Save

Note: GitHub Pages doesn't directly support running Python applications. You'll need to use a service like Streamlit Sharing, Heroku, or other cloud platforms that support Python web applications.

## Usage

1. Use the sidebar to input the RMR parameters:
   - Select the appropriate option for each parameter based on your rock mass conditions
   - Input the excavation dimensions and tunnel length

2. View the calculated RMR value and rock mass classification in the "RMR Calculator" tab

3. Check the recommended support system in the "Support Recommendations" tab

4. Learn more about RMR in the "About RMR" tab

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Z.T. Bieniawski for developing the RMR system
- Streamlit for providing the framework for this web application
