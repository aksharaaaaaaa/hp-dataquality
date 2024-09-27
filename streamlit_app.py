import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.stylable_container import stylable_container
import plotly.express as px

hp_data = Path(__file__).parent/'data/train.csv'
hp_df = pd.read_csv(hp_data)

st.title("Data Quality Assessment - House Prices :house_buildings:")

st.divider()

st.header(':blue[Data completeness]', help='Count null values in each column')

labels = hp_df.columns.tolist()

total_null_values = hp_df.isnull().sum()
total_values = hp_df.isnull().sum() + hp_df.notnull().sum()
#hp_df.count().sort_values(ascending=True)
not_null_values = hp_df.notnull().sum()
null_values_percentage = (total_null_values/total_values)*100

missing_values = pd.concat({'Null': total_null_values, 'Not_null': not_null_values}, axis=1)#, 'Percentage_missing': null_values_percentage}, axis=1)
missing_values = missing_values.transpose()
missing_values.reset_index()
miss = pd.concat({'Null': total_null_values, 'Not_null': not_null_values, 'Percentage_missing': null_values_percentage}, axis=1)

#st.dataframe(dataframe_explorer(miss,case=False))

miss_noindex = miss.reset_index()

chart = alt.Chart(miss_noindex).mark_bar().encode(
    x=alt.X(miss_noindex.columns[3], type='quantitative', title='Percentage missing (%)'),
    y=alt.Y(miss_noindex.columns[0], type='nominal', title='Column')).properties(title='Missing data (all columns)')
text = alt.Chart(miss_noindex).mark_text(dx=15,dy=3,color='white').encode(
    x=alt.X(miss_noindex.columns[3], type='quantitative'),
    y=alt.Y(miss_noindex.columns[0], type='nominal'),
    text=alt.Text('Percentage_missing', format='.1f'))
st.altair_chart(chart+text, use_container_width=True)

st.info('The following columns intentionally contain NA values as non-applicable attributes:  \n\n Alley, BsmtQual, BsmtCond, BsmtExposure, BsmtFinType1, BsmtFinType2, FireplaceQu, GarageType, GarageFinish, GarageQual, GarageCond, PoolQC, Fence, MiscFeature',
        icon="⚠️")

NA_allowed_columns = ['Alley','BsmtQual','BsmtCond','BsmtExposure','BsmtFinType1',
                      'BsmtFinType2','FireplaceQu','GarageType','GarageFinish',
                      'GarageQual','GarageCond','PoolQC','Fence','MiscFeature']

actual_NA_cols = []
for y in hp_df.columns:
    if y not in NA_allowed_columns:
        actual_NA_cols.append(y)


cols1= []
nulls1 = []
null_percent = []
for z in hp_df.columns:
    cols1.append(z)
    if z in actual_NA_cols:
        x = hp_df[z].isnull().sum()
    else:
        x = int('0')
    nulls1.append(x)
    null_df1 = pd.DataFrame({'C':cols1,'N':nulls1})
    
null_df1['P'] = (null_df1['N']/len(hp_df))*100
null_df = null_df1.drop(null_df1[null_df1['N'] == 0].index)

chart = alt.Chart(null_df).mark_bar().encode(
    x=alt.X(null_df.columns[2], type='quantitative', title='Percentage missing (%)'),
    y=alt.Y(null_df.columns[0], type='nominal', title='Column')).properties(title='Missing data (actual nulls)')
text = alt.Chart(null_df).mark_text(dx=15,dy=3,color='white').encode(
    x=alt.X(null_df.columns[2], type='quantitative'),
    y=alt.Y(null_df.columns[0], type='nominal'),
    text=alt.Text('P', format='.1f'))
st.altair_chart(chart+text, use_container_width=True)


has_null = hp_df[actual_NA_cols].isna().any(axis=1)
rows_with_null = has_null.sum()

col1,col2 = st.columns(2)
with col1:
    lcont = stylable_container(key="cont1",
                               css_styles="""
                               {
                               background-color: rgba(65, 135, 220, 0.1);
                               color: white;
                               border: 2px solid rgba(100, 140, 200, 0.8);
                               border-radius: 10px;
                               padding: calc(1em - 1px)}""")
    lcont.write(':blue[Total rows processed]')
    lcont.text(len(hp_df))
with col2:
    rcont = stylable_container(key="cont2",
                               css_styles="""
                               {
                               background-color: rgba(220, 65, 70, 0.1);
                               color: white;
                               border: 2px solid rgba(210, 95, 95, 0.8);
                               border-radius: 10px;
                               padding: calc(1em - 1px)}""")
    rcont.write(':red[Incomplete rows]')
    rcont.text(rows_with_null)


################################################################################
### OUTLIERS

st.divider()
st.header(':red[Outliers & statistics]',help = 'Identify outliers in each column')

num_cols = ['Id','MSSubClass','LotFrontage','LotArea','OverallQual',
            'OverallCond','YearBuilt','YearRemodAdd','MasVnrArea',
            'BsmtFinSF1','BsmtFinSF2','BsmtUnfSF','TotalBsmtSF',
            '1stFlrSF','2ndFlrSF','LowQualFinSF','GrLivArea',
            'BsmtFullBath','BsmtHalfBath','FullBath','HalfBath',
            'BedroomAbvGr','KitchenAbvGr','TotRmsAbvGrd','Fireplaces',
            'GarageYrBlt','GarageCars','GarageArea','WoodDeckSF',
            'OpenPorchSF','EnclosedPorch','3SsnPorch','ScreenPorch',
            'PoolArea','MiscVal','MoSold','YrSold']

tablist = st.tabs(num_cols)

for i in range(len(tablist)):  # Use index for clarity
    with tablist[i]:
        fig = px.box(hp_df, x=num_cols[i], orientation='h',hover_data=['Id'], points='all', color_discrete_sequence=px.colors.qualitative.Pastel1)
        st.plotly_chart(fig)

col_stats = stylable_container(key="cont3",
                               css_styles="""
                               {
                               background-color: rgba(220, 65, 70, 0.1);
                               color: white;
                               border: 2px solid rgba(210, 95, 95, 0.8);
                               border-radius: 5px;
                               padding: calc(1em - 1px)}""")
with col_stats:
    col_stats.subheader('Summary of column statistics')
    col_stats.dataframe(hp_df.describe(), width = 670)#,use_container_width=True)

#####################################################################
st.divider()
st.header(':green[Data uniqueness]', help='Identify duplicated rows within data')

# unique value count in each column
uniques = hp_df.nunique(axis='index').rename_axis("Columns").rename("Unique values")
st.dataframe(uniques, use_container_width=True)

# count duplicated rows
dupes = hp_df.drop(columns=['Id'], axis=0).duplicated()
st.write(f'The dataset contains :green[{dupes.sum()}] duplicated rows.')

