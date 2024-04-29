# %% [markdown]
# # What makes a population truly happy?
#
# Happiness can mean different things for different people. For some, financial security can give them happiness, while for others the ability to roam freely without any financial safety might be a more fulfilling lifestyle. The human experience cannot be measured on a common scale or summed into a definitive bracket. So, how do we measure happiness? The World Happiness Report, a partnership of Gallup, the Oxford Wellbeing Research Centre, the UN Sustainable Development Solutions Network, and the WHR’s Editorial Board, is an attempt at quantifying and assessing the collective happiness of populations around the world. Respondents from every country to a survey conducted by Gallup are asked to imagine their happiness in life as a ladder ranging from 0 to 10, and are asked to guage their place on the ladder. The average of these scores are calculated as the collective Happiness Score of the country. The World Happiness Report also provides data on 6 metrics that can be used to explain the happiness score.

# %%
import pandas as pd
import numpy as np

import altair as alt
import streamlit as st
import json

# %% [markdown]
# ## Data Preprocessing

# %%
st.title("What makes a population happy? Decoding the World Happiness Report")
st.caption("A data-driven exploration by Shriya Ejanthker and Christopher Kok")
st.write(
    """
    \n
    The pursuit of happiness is a fundamental human goal, and understanding what makes a population truly happy is crucial for policymakers, organizations, and individuals alike. 
    Happiness can mean different things for different people. For some, financial security can give them happiness, while for others the ability to roam freely without any financial safety might be a more fulfilling lifestyle. 
    What makes people truly happy at a global scale? Is it something we can count or measure, or is our joy more of a vague, intangible feeling? The human experience cannot be measured on a common scale or summed into a definitive bracket. 
    So, how do we measure happiness? 
    Welcome to an exploratory article on the World Happiness Index!
    The World Happiness Report, a partnership of Gallup, the Oxford Wellbeing Research Centre, the UN Sustainable Development Solutions Network, and the WHR’s Editorial Board, is an attempt at quantifying and assessing the collective happiness of populations around the world. 
    Respondents from 153 countries to a survey conducted by Gallup are asked to imagine their happiness in life as being on a ladder with rungs from 0 to 10, and are asked to guage their place on the ladder. 
    The average of these scores are calculated as the collective Happiness Score of the country. 
    The World Happiness Report also provides data on 6 metrics that can be used to explain the happiness score, namely economic strength (measured by GDP per capita), social support, life expectancy, freedom to make life choices, generosity, and perceptions of corruption. 
    Gallup calculates how much of the happiness score can be attributed to these metrics.
    Understanding these metrics and the role they play in our happiness can foster the blueprint for a healthy society.

    First let's take a look at the happiest countries in the world in the figure below. Slide the slider to see the leaderboard of happy countries change. 
    It is observable that the nordic countries seem to dominate this leaderboard, which begs the question, what are they doing different? What makes them so happy?
    Finland, the happiest country in the world, exemplifies the importance of robust social welfare systems, excellent healthcare, and high levels of mutual trust within the community. The Finnish culture highly values personal freedom and outdoor activities, contributing to both physical and mental well-being.
    Finland's policies are socialist in nature, as with the rest of the nordic region. They emphasize social welfare, and personal autonomy.
    Finland has one of the highest GDP per capita's, signifying equitable distribution of wealth, which translates to a good standard of living for its residents.
    It also provides free healthcare to all, regardless of insurance or employment, and the government covers the costs of education from preschool to university.
    The Finnish culture is also known for its emphasis on personal freedom and outdoor activities, which contribute to both physical and mental well-being.
    Being a close-knit community, the Finnish people have high levels of mutual trust, which is also a key factor in happiness.
    All of this certainly sets the Finnish apart from say, the United States, which has albeit a higher GDP per capita, but is known as a capitalist society with high levels of income inequality, and a healthcare system that is not accessible to all.
    Finland is proof that a society that values social welfare, personal autonomy, and mutual trust can foster a happier population.
    The rest of the world could certainly take a page out of the Finnish book to foster a healthier, happier society.
    But is it really that simple? Can we just copy the Finnish model and expect the same results?
"""
)

# %%
# data for 2024
df_2024 = pd.read_csv("WHR2024.csv")

# %%
# get the data from 2013-2023
df_years = pd.read_csv("WorldHappinessIndex2013-2023.csv")
df_years.sort_values(by=["Rank"], inplace=True)

# %%
df_2024 = df_2024[
    [
        "Country name",
        "Ladder score",
        "Explained by: Log GDP per capita",
        "Explained by: Social support",
        "Explained by: Healthy life expectancy",
        "Explained by: Freedom to make life choices",
        "Explained by: Generosity",
        "Explained by: Perceptions of corruption",
        "Dystopia + residual",
    ]
]
df_2024 = df_2024.rename(
    columns={
        "Country name": "Country",
        "Ladder score": "Happiness Score",
        "Explained by: Log GDP per capita": "GDP per capita",
        "Explained by: Social support": "Social Support",
        "Explained by: Healthy life expectancy": "Healthy Life Expectancy",
        "Explained by: Freedom to make life choices": "Freedom",
        "Explained by: Generosity": "Generosity",
        "Explained by: Perceptions of corruption": "Government Trust",
    }
)
df_2024["Rank"] = df_2024["Happiness Score"].rank(ascending=False)
df_2024_years = df_2024[["Country", "Happiness Score", "Rank"]].copy()
df_2024_years["Year"] = 2024
df_years.rename(columns={"Index": "Happiness Score"}, inplace=True)
df_years = pd.concat([df_years, df_2024_years])
df_years.dropna(inplace=True)
df_years = df_years[df_years["Year"] != 2014]
df_years = df_years[df_years["Year"] != 2013]


# %% [markdown]
# ## Finding happiest countries in the world and their happiness breakdown

# %%
# Chart for left side, top 10 happiest countries
df_top10 = df_years[df_years["Rank"] <= 10]

# Create a slider for the Year
slider = alt.binding_range(min=2015, max=2024, step=1, name="Year: ")
select_year = alt.selection_single(fields=["Year"], bind=slider, value=2024)

# Create the chart
chart = (
    alt.Chart(df_top10)
    .mark_bar(color="darkorange")
    .encode(
        y=alt.Y(
            "Country:N",
            sort="-x",
            title=None,
            axis=alt.Axis(grid=False, ticks=False, labelPadding=8),
        ),
        x=alt.X(
            "Happiness Score:Q",
            scale=alt.Scale(domain=[0, 9]),
            title="Happiness Score",
            axis=alt.Axis(grid=False),
        ),
        tooltip=["Country", "Happiness Score", "Rank"],
    )
    .transform_filter(select_year)
    .add_params(select_year)
    .properties(
        width=350,
        height=250,
        title=alt.Title("Top 10 Happiest Countries in the World", anchor="middle"),
    )
)


# %%
# Chart for right side, top 10 happiest countries in 2024 and their happiness score breakup
df_2024_top10 = df_2024[df_2024["Rank"] <= 10].copy()
metrics = [
    "Social Support",
    "Healthy Life Expectancy",
    "Government Trust",
    "Generosity",
    "GDP per capita",
    "Freedom",
    "Dystopia + residual",
]
df_2024_top10 = df_2024_top10[
    [
        "Country",
        "GDP per capita",
        "Social Support",
        "Healthy Life Expectancy",
        "Freedom",
        "Generosity",
        "Government Trust",
        "Dystopia + residual",
    ]
]
df_2024_explained = df_2024_top10.melt(
    id_vars="Country", var_name="Metric", value_name="Happiness Score Breakup"
)

countries_explained = (
    alt.Chart(df_2024_explained)
    .mark_bar()
    .encode(
        x=alt.X(
            "Happiness Score Breakup:Q",
            axis=alt.Axis(labelPadding=3, grid=False, title="Happiness Score"),
            scale=alt.Scale(domain=[0, 9]),
        ),
        y=alt.Y(
            "Country:N",
            title=None,
            axis=alt.Axis(ticks=False, labelPadding=8),
            sort="-x",
        ),
        color=alt.Color("Metric:N", sort=metrics),
        order=alt.Order("Metric:N", sort="descending"),
        tooltip=["Country", "Metric", "Happiness Score Breakup"],
    )
    .properties(
        width=350,
        height=250,
        title=alt.Title(
            "Happiness Score Breakup of Happiest Countries in 2024", anchor="middle"
        ),
    )
)

# %%
chart1 = (chart | countries_explained).configure_view(stroke=None)
chart1

# %%
st.caption(
    "Figure 1: The top 10 happiest countries in the world in 2024 and their happiness score breakup. Slide the slider to see the leaderboard of happy countries change."
)
st.caption("Source: World Happiness Report 2015-2024")

# %%
st.write(
    """
    Upon examining the breakup of the happiness score of the top 10 happiest countries in 2024, we can see that the metrics that contribute most to the happiness score are GDP per capita, social support, and freedom. 
    That begs the question, is money, social life, and freedom the key to happiness?
    These three are surely important, that is indisputable by now.
    Upon oberving the changes in the leaderboard, Switzerland seems to drop down from first place in 2015 to ninth place in 2024. What changed? Switzerland still has one of the highest GDP per capita's in the world, and similar policies to finland.
    It is of notable interest that Swiss politics has been shifting towards the right, with rising wariness of immigration and minority groups in the country.
    It can also be said that Switzerland has had tough competition from its nordic neighbours, and might have been disproportionately affected by the pandemic.
    Looking at the breakup of the happiness score, we can see that both Finland and Switzerland have an almost identical breakup, with the only difference being made up by the residual, which simply stands for unexplained miscellaneous factors.
    So what are the finnish doing more that the swiss are not? Why are the Finns see themselves as happier than the Swiss despite having similar policies and identical scores on happiness indicators? Can this difference be a matter of difference in culture?
    This leaves one to ponder, how much does our culture influence our view of happiness and the things we place value on?
"""
)

# %% [markdown]
# ## Finding the correlation of metrics with happiness

# %%
st.subheader("Understanding the role of different variables in happiness")

# %%
# contribution of each metric to the happiness score
df_2024["GDP per capita_contribution"] = (
    df_2024["GDP per capita"] / df_2024["Happiness Score"]
)
df_2024["Social Support_contribution"] = (
    df_2024["Social Support"] / df_2024["Happiness Score"]
)
df_2024["Healthy Life Expectancy_contribution"] = (
    df_2024["Healthy Life Expectancy"] / df_2024["Happiness Score"]
)
df_2024["Freedom_contribution"] = df_2024["Freedom"] / df_2024["Happiness Score"]
df_2024["Generosity_contribution"] = df_2024["Generosity"] / df_2024["Happiness Score"]
df_2024["trust_contribution"] = df_2024["Government Trust"] / df_2024["Happiness Score"]


# %%
# correlation matrix
spearman_cormatrix = df_2024[
    [
        "Happiness Score",
        "GDP per capita",
        "Social Support",
        "Healthy Life Expectancy",
        "Freedom",
        "Generosity",
        "Government Trust",
    ]
].corr(method="spearman")

# %%
heatmap_df = (
    spearman_cormatrix.stack()
    .reset_index()
    .rename(
        columns={0: "correlation", "level_0": "Variable 1", "level_1": "Variable 2"}
    )
)
base = alt.Chart(heatmap_df).encode(
    x=alt.X(
        "Variable 2:O",
        axis=alt.Axis(
            grid=False, title=None, ticks=False, labelAngle=-45, labelPadding=10
        ),
    ),
    y=alt.Y(
        "Variable 1:O",
        axis=alt.Axis(grid=False, title=None, ticks=False, labelPadding=10),
    ),
)

# Text layer with correlation labels
# Colors are for easier readability
text = base.mark_text().encode(
    text=alt.Text("correlation:Q", format=".2f"),
    color=alt.condition(
        alt.datum.correlation > 0.5, alt.value("white"), alt.value("black")
    ),
)

# The correlation heatmap itself
cor_plot = base.mark_rect().encode(
    color=alt.Color("correlation:Q", scale=alt.Scale(scheme="reds"))
)
heatmap = (cor_plot + text).properties(
    width=350, height=250, title=alt.Title("Correlation Heatmap", anchor="middle")
)
# heatmap

# %%
spearman_cormatrix = spearman_cormatrix.drop(
    [
        "GDP per capita",
        "Social Support",
        "Healthy Life Expectancy",
        "Freedom",
        "Generosity",
        "Government Trust",
    ],
    axis=1,
)
spearman_cormatrix.drop("Happiness Score", axis=0, inplace=True)
spearman_cormatrix.reset_index(inplace=True)
spearman_cormatrix.rename(
    columns={"index": "Factor", "Happiness Score": "Correlation with Happiness Score"},
    inplace=True,
)
spearman_cormatrix.sort_values(
    by="Correlation with Happiness Score", ascending=False, inplace=True
)

# %%
# Chart for top factors
top_factors = (
    alt.Chart(spearman_cormatrix)
    .mark_bar(color="teal")
    .encode(
        x=alt.X(
            "Correlation with Happiness Score:Q",
            axis=alt.Axis(labelPadding=3, grid=False),
        ),
        y=alt.Y(
            "Factor:N",
            title=None,
            axis=alt.Axis(ticks=False, labelPadding=15),
            sort="-x",
        ),
        tooltip=["Factor", "Correlation with Happiness Score"],
    )
    .properties(
        width=350, height=250, title="Top Metrics Correlated with Happiness Score"
    )
)
# top_factors

# %%
chart2 = (top_factors | heatmap).configure_view(stroke=None)
chart2

# %%
st.caption(
    "Figure 2: The metrics ranked by their correlation with the Happiness Score, and the correlation heatmap of the metrics. The heatmap shows the correlation between the metrics."
)
st.caption("Source: World Happiness Report 2024")

# %%
st.write(
    """
    Let's take a look at the correlation heatmap and the top metrics correlated with the happiness score to understand the global view on happiness, and what things us humans as a whole as a whole place value on.
    The above is a correlation matrix - it's a bit of a fancy term for a chart that shows how much various things are related to each other. And in our case, we're talking about happiness. What we find looking at the correlation with the happiness score is that certain factors seem to pack quite a punch when it comes to influencing how happy people are. 
    GDP (which is more or less a measure of economic success), social support (think friends, family, and community), and life expectancy seem to have a big impact.
    It makes sense, right? Being financially secure, surrounded by a supportive network, and having a long, healthy life all seem to be elements of a happy picture. But, things get a bit twisty when 'freedom' gets added to the mix. It doesn't just correlate with happiness—it gets involved with all the other factors too. 
    Freedom is fundamental (you need it to pursue what makes you happy) but, its correlation with so many other aspects presents a bit of a chicken-and-egg situation: does freedom induce happiness or does being happier make us feel freer? 
    And here's another twist! Trust in government only has a so-so connection with happiness. Government trust, meanwhile, showed only a mediocre correlation with happiness, stirring debates about its intrinsic worth in ensuring societal wellbeing. 
    
    This brings us to the conclusion - correlation doesn't mean causation. Just because a few factors are highly correlated with happiness does not mean they cause happiness itself. 
    This is important, as it highlights that happiness is a complex concept that cannot be reduced to a single metric. 
    But what the World Happiness Report does achieve is it shows that happiness is not just a personal feeling, but also a social and economic issue that can be measured and analyzed.
    By using data and evidence, we can better understand what makes people happy and create a happier world for everyone!
"""
)

# %% [markdown]
# ### Does money buy happiness?

# %%
st.subheader("Does money buy happiness?\n")

# %%
# To get the categories for each metric
df_2024_factors = df_2024[
    [
        "Country",
        "Happiness Score",
        "GDP per capita",
        "Social Support",
        "Healthy Life Expectancy",
        "Freedom",
        "Generosity",
        "Government Trust",
        "Dystopia + residual",
    ]
].copy()
categories = ["Low", "Average", "High"]
df_2024_factors["GDP per capita_category"] = pd.qcut(
    df_2024_factors["GDP per capita"], q=3, labels=categories
)
df_2024_factors["Social Support_category"] = pd.qcut(
    df_2024_factors["Social Support"], q=3, labels=categories
)
df_2024_factors["Healthy Life Expectancy_category"] = pd.qcut(
    df_2024_factors["Healthy Life Expectancy"], q=3, labels=categories
)
df_2024_factors["Freedom_category"] = pd.qcut(
    df_2024_factors["Freedom"], q=3, labels=categories
)
df_2024_factors["Generosity_category"] = pd.qcut(
    df_2024_factors["Generosity"], q=3, labels=categories
)
df_2024_factors["Government Trust_category"] = pd.qcut(
    df_2024_factors["Government Trust"], q=3, labels=categories
)
df_2024_factors["Happiness Score_category"] = pd.qcut(
    df_2024_factors["Happiness Score"], q=3, labels=categories
)

# %%
# Regression plot for GDP per capita vs Happiness Score
scatter = (
    alt.Chart(df_2024_factors.reset_index())
    .mark_circle()
    .encode(
        x=alt.X(
            "GDP per capita:Q", title="Log GDP per capita", axis=alt.Axis(grid=False)
        ),
        y=alt.Y(
            "Happiness Score:Q", axis=alt.Axis(grid=False), title="Happiness Score"
        ),
        color=alt.Color(
            "Happiness Score_category:N",
            scale=alt.Scale(scheme="category10", domain=categories),
            legend=alt.Legend(title="Happiness"),
        ),
        tooltip=["Country:N", "Happiness Score:Q"],
    )
    .properties(title="Happiness Score vs GDP per capita")
)

reg = (
    scatter.transform_regression("GDP per capita", "Happiness Score")
    .mark_line(strokeWidth=2)
    .encode(color=alt.value("black"))
)

chart = (scatter + reg).configure_view(stroke=None)
chart

# %%
st.caption(
    "Figure 3: Move the mouse over the scatter points to see where different countries lie on the GDP per capita vs Happiness Score plot. The black line represents the regression line."
)
st.caption("Source: World Happiness Report 2024")

# %%
st.write(
    """
Taking a look at the figure above, we can see that there is a very clear positive correlation between GDP per capita and happiness score. This absolutely makes sense, as money can enable people to buy the things they need.
But, we can also see that there are outliers in this plot. For example, Nicaragua has a relatively low GDP per capita but a high happiness score. This could be due to the country's strong sense of community and social support, which can compensate for the lack of financial resources. 
On the other hand, we have Turkiye or Turkey, which have a very high GDP per capita but a relatively low happiness score. This could be due to the country's high income inequality and lack of social support.
This tells us that money can buy happiness most of the times yes, but not always. And certainly not for everyone. 
It brings us back to the notion that different cultures and societies place value on different things, and that culture has something to do with how we perceive happiness.
"""
)

# %% [markdown]
# ## Interactive Dashboard

# %%
st.subheader("A global view on happiness\n")

# %%
st.markdown(
    """ The interactive dashboard above shows the happiness score of countries around the world, color-coded by the level of happiness.  
    For example, if you select 'High' in the dropdown menu for GDP per capita, you can see which countries have a high GDP per capita and how that affects their happiness score. 
    This can help us understand how different countries are affected by the metrics that contribute to happiness, and how that affects their overall happiness score.
    This is a great way to understand the global view on happiness and how different countries place value on different things. 
    By understanding this, we can create a happier world for everyone!
    
            Select the category of the metric you want to view below to filter the countries by different metrics!
"""
)

# %%
import country_converter as coco
from vega_datasets import data

# map for the world happiness index for 2024
df_2024_factors["Country_iso_numeric"] = df_2024_factors["Country"].apply(
    lambda x: coco.convert(names=x, to="isocode")
)

menu = [
    "High",
    "Average",
    "Low",
]


# function to create selection
def create_selection(category_name):
    labels = [option + " " for option in menu]
    dropdown = alt.binding_select(
        options=[None] + menu, labels=["All"] + labels, name=f"{category_name}:  "
    )
    selection = alt.selection_point(
        fields=[f"{category_name}_category"], bind=dropdown, clear="click"
    )
    return selection


gdp_selection = create_selection("GDP per capita")
social_support_selection = create_selection("Social Support")
healthy_life_expectancy_selection = create_selection("Healthy Life Expectancy")
freedom_selection = create_selection("Freedom")
generosity_selection = create_selection("Generosity")
trust_selection = create_selection("Government Trust")

# World map
world = alt.topo_feature(data.world_110m.url, "countries")
world_base = (
    alt.Chart(world)
    .mark_geoshape(fill="lightgray", stroke="black")
    .transform_filter((alt.datum.id != 10) & (alt.datum.id != 304))
)

# World map with metrics
world_factors = (
    alt.Chart(world)
    .mark_geoshape(stroke="black", strokeWidth=0.3)
    .encode(
        color=alt.Color(
            "Happiness Score_category:N",
            scale=alt.Scale(domain=menu, scheme="viridis", reverse=True),
            title="Happiness Score",
        ),
        tooltip=[
            "Country:N",
            "Happiness Score:Q",
            alt.Tooltip("GDP per capita_category:N", title="GDP per capita"),
            alt.Tooltip("Social Support_category:N", title="Social Support"),
            alt.Tooltip(
                "Healthy Life Expectancy_category:N", title="Healthy Life Expectancy"
            ),
            alt.Tooltip("Freedom_category:N", title="Freedom"),
            alt.Tooltip("Generosity_category:N", title="Generosity"),
            alt.Tooltip("Government Trust_category:N", title="Government Trust"),
        ],
    )
    .transform_lookup(
        lookup="id",
        from_=alt.LookupData(
            df_2024_factors,
            "Country_iso_numeric",
            [
                "Happiness Score",
                "Country",
                "Happiness Score_category",
                "GDP per capita_category",
                "Social Support_category",
                "Healthy Life Expectancy_category",
                "Freedom_category",
                "Generosity_category",
                "Government Trust_category",
            ],
        ),
    )
    .transform_filter((alt.datum.id != 10) & (alt.datum.id != 304))
    .transform_filter(gdp_selection)
    .add_params(
        gdp_selection,
        social_support_selection,
        healthy_life_expectancy_selection,
        freedom_selection,
        generosity_selection,
        trust_selection,
    )
    .transform_filter(social_support_selection)
    .transform_filter(healthy_life_expectancy_selection)
    .transform_filter(freedom_selection)
    .transform_filter(generosity_selection)
    .transform_filter(trust_selection)
    .properties(title=alt.Title("Happiness Score Dashboard"), width=900, height=600)
    .project(type="mercator")
)
world_map = (
    (world_base + world_factors)
    .configure_view(stroke=None)
    .configure_title(fontSize=15, anchor="middle", color="black", offset=10)
    .configure_legend(symbolStrokeWidth=0, padding=10)
)
world_map

# %%
st.caption("Figure 4")
st.caption("Source: World Happiness Report 2024")

st.write(
    """
         Upon simply looking at the world map, we can see that the countries that are the happiest in the world are in Europe and North America, and including Australia and New Zealand, these countries would form the 'First World'.
         Is it true then? First World countries are happier than Third World countries? One could argue not, as Khazakhstan has a higher happiness score than Portugal. 
         There's also exceptions to the rule like Chile, having undergone decades of dictatorship, and also Saudi Arabia, a country known for its strict laws and lack of freedom, but still has a high happiness score.
         The 'first world' countries are simply countries that have had the luxury of time and resources to focus on happiness, while the 'third world' countries have had to focus on survival.
         Centuries of colonization and exploitation have left these countries with a lack of resources and infrastructure, and the people have had to focus on survival rather than happiness.
         But as we saw, countries like Chile and Saudi Arabia where they have high social support shows that community and togetheress can overcome the biggest of adversities.
         
        Interacting with the dashboard above, we can see that uzbekistan and nicaragua have a high happiness score despite having a low GDP per capita. 
        Upon moving the mouse over the countries, we can see that both these countries have high trust in their governments and freedom to make their own choices.
        Similarly, for low GDP per capita, we can see that Turkey has high income but low freedom. Money is important, but you won't truly be happy if you cannot do what you want with it.
        Further filtering by high government trust, we see that Japan is the only unhappy country on the map, and has high scores on every metric except for generosity and average in freedom. 
        This would lead us to think that freedom is a key factor in happiness, but a country like Slovakia has low freedom, generosity, and trust, but scores high in GDP per capita, social support, and healthy life expectancy.
        Thus, we can clearly see that different countries value certain metrics more than other countries, and culture indeed is a big part of it. 
         
"""
)

# %% [markdown]
# ## Happiness trends of countries and metrics most important to them

# %%
st.subheader("Historic Trends of Happiness")

# %%
# Create a selection that chooses the nearest point & selects based on x-value
selection_year = alt.selection_point(
    fields=["Year"], nearest=True, on="mouseover", empty=False
)
country_dropdown = alt.binding_select(
    options=sorted(df_years["Country"].unique()), name="Select Country  "
)
selection_country = alt.selection_point(
    fields=["Country"], bind=country_dropdown, value="Afghanistan"
)

# Line chart for the happiness score by year
line = (
    alt.Chart(df_years)
    .mark_line(interpolate="basis")
    .encode(
        x=alt.X("Year:O", axis=alt.Axis(title="Year", labelAngle=0)),
        y=alt.Y(
            "Happiness Score:Q",
            axis=alt.Axis(title="Happiness Score", grid=False),
            scale=alt.Scale(domain=[1, 10]),
        ),
    )
    .add_params(selection_country)
    .transform_filter(selection_country)
    .properties(
        width=400,
        height=250,
        title=alt.Title(text="Happiness Score by Year", anchor="middle"),
    )
)

# Point chart to highlight selected year
point = (
    alt.Chart(df_years)
    .mark_point(color="black", size=10)
    .encode(
        x=alt.X("Year:O", axis=alt.Axis(title="Year", labelAngle=0)),
        y=alt.Y(
            "Happiness Score:Q",
            axis=alt.Axis(title="Happiness Score"),
            scale=alt.Scale(domain=[1, 10]),
        ),
        opacity=alt.condition(selection_year, alt.value(1), alt.value(0)),
    )
    .transform_filter(selection_country)
    .add_params(selection_year)
    .properties(width=400, height=250)
)

# Text chart to show the happiness score
text = (
    alt.Chart(df_years)
    .mark_text(align="left", dy=-15)
    .encode(
        x=alt.X("Year:O", axis=alt.Axis(title="Year", labelAngle=0)),
        y=alt.Y(
            "Happiness Score:Q",
            axis=alt.Axis(title="Happiness Score"),
            scale=alt.Scale(domain=[1, 10]),
        ),
        text=alt.Text("Happiness Score:Q", format=".1f"),
        opacity=alt.condition(selection_year, alt.value(1), alt.value(0)),
    )
    .transform_filter(selection_country)
)


# %%
# Contribution of each metric to the happiness score
df_contribution = df_2024[
    [
        "Country",
        "GDP per capita_contribution",
        "Social Support_contribution",
        "Healthy Life Expectancy_contribution",
        "Freedom_contribution",
        "Generosity_contribution",
        "trust_contribution",
    ]
]
df_contribution = df_contribution.rename(
    columns={
        "GDP per capita_contribution": "GDP per capita",
        "Social Support_contribution": "Social Support",
        "Healthy Life Expectancy_contribution": "Healthy Life Expectancy",
        "Freedom_contribution": "Freedom",
        "Generosity_contribution": "Generosity",
        "trust_contribution": "Government Trust",
    }
)
df_contribution = df_contribution.melt(
    id_vars="Country", var_name="Factor", value_name="Share of Happiness Score"
)

# Most important metrics
countries_contributions = (
    alt.Chart(df_contribution)
    .mark_bar(color="darkorange")
    .encode(
        x=alt.X(
            "Share of Happiness Score:Q",
            axis=alt.Axis(labelPadding=3, grid=False, format="%"),
            scale=alt.Scale(domain=[0, 0.5]),
        ),
        y=alt.Y(
            "Factor:N",
            title=None,
            axis=alt.Axis(ticks=False, labelPadding=8),
            sort="-x",
        ),
    )
    .transform_filter(selection_country)
    .properties(
        width=400,
        height=250,
        title=alt.Title(text="Most Important Metrics", offset=10, anchor="middle"),
    )
)

countries_contributions_text = countries_contributions.mark_text(
    align="left", baseline="middle", dx=3
).encode(text=alt.Text("Share of Happiness Score:Q", format=".2%"))

countries_factors = countries_contributions + countries_contributions_text

country_history = (
    alt.hconcat((line + point + text), countries_factors)
    .resolve_scale(y="independent")
    .configure_view(stroke=None)
)
country_history


# %%
st.caption(
    "Figure 5: Select a country from the dropdown menu to see the happiness score by year and the metrics that are most important to the country."
)
st.caption("Source: World Happiness Report 2015-2024")

st.write(
    """
       We saw the example of Chile above, and here upon selecting it we can see that Chile places almost as much value on social support as on money. 
        It has consistenly maintained its happiness, with a little dip in 2020 which can be attributed to the pandemic. Chile's example gives us hope as it is a country that has recently overcome a fascist regime then turned a new leaf.
        We can also confirm that Uzbekistan places more importance on social support than money, and has also been more or less consistent.
        China is a country that has seen a steady increase in happiness, and places more importance on money than social support. This could be due to the country's rapid economic growth and the government's focus on economic development.
        
        Coming to the United States, it is unfortunate to see that the country has seen a steady decline in happiness over the years. As compared to Finland, the US places lesser importance on social support, freedom and government trust. 
        Maybe the US should look inwards as a country and ask ourselves, are we heading in the right direction? What do we want as a nation?
"""
)

# %% [markdown]
# ## Happiness Trend around the Globe

# %%
st.subheader("How has the world progressed over the last decade?")
st.write(
    """Below is a globe with countries color-coded by their relative happiness to their own average happiness over the last decade. This will give us a view of whether countries have gotten happier or sadder in comparison with themselves. 
         Drag the slider across to see the world change!"""
)

# %%
# get the mean happiness score for each country
df_years["Mean_Country"] = df_years.groupby("Country")["Happiness Score"].transform(
    "mean"
)
df_years["Difference_Country"] = df_years["Happiness Score"] - df_years["Mean_Country"]
df_years.head()

# get the mean for each year and the difference from the mean
df_years["Mean_Year"] = df_years.groupby("Year")["Happiness Score"].transform("mean")
df_years["Difference_Year"] = df_years["Happiness Score"] - df_years["Mean_Year"]


# %%
# store iso and iso_numeric codes for each country
df_years["iso"] = coco.convert(names=df_years["Country"], to="ISO3")
df_years["iso_numeric"] = coco.convert(names=df_years["Country"], to="isocode")

# %%
# World map for the difference in happiness score for each country
world_years = df_years[["iso_numeric", "Difference_Country", "Year", "Country"]].copy()
world_years["Year"] = world_years["Year"].astype(int).astype(str)

world_years = world_years.drop_duplicates(["iso_numeric", "Year"])
world_years = world_years.pivot(
    index=["iso_numeric", "Country"], columns="Year", values="Difference_Country"
).reset_index()
world_years.head()
columns = [str(year) for year in range(2013, 2025)]

# Create a slider for the Year
slider = alt.binding_range(min=2015, max=2024, step=1, name="Year: ")
select_year = alt.selection_single(
    name="Year", fields=["Year"], bind=slider, value=2015
)

# Create a globe chart
world = alt.topo_feature(data.world_110m.url, "countries")
sphere = alt.sphere()
graticule = alt.graticule()

map2 = (
    alt.Chart(world)
    .mark_geoshape(stroke="black", strokeWidth=0.05)
    .transform_lookup(
        lookup="id",
        from_=alt.LookupData(world_years, "iso_numeric", columns + ["Country"]),
    )
    .transform_fold(columns, as_=["Year", "Difference_Country"])
    .transform_calculate(
        Year="parseInt(datum.Year)",
        Difference_Country="isValid(datum.Difference_Country) ? datum.Difference_Country : -1",
        # Country='datum.Country'
    )
    .encode(
        color=alt.condition(
            "datum.Difference_Country > -1",
            alt.Color(
                "Difference_Country:Q",
                scale=alt.Scale(scheme="redyellowgreen", domain=[-1, 1]),
                legend=alt.Legend(title="Relative Happiness"),
            ),
            alt.value("#dbe9f6"),
        ),
        tooltip=[
            "Country:N",
            alt.Tooltip(
                "Difference_Country:Q", format=".2f", title="Relative Happiness"
            ),
        ],
    )
    .add_selection(select_year)
    .transform_filter(select_year)
)

globe = alt.Chart(sphere).mark_geoshape(fill="lightblue")
grid = alt.Chart(graticule).mark_geoshape(stroke="white", strokeWidth=0.5)

world_map = (
    (globe + grid + map2)
    .project("naturalEarth1")
    .properties(
        width=900,
        height=600,
        title=alt.Title(
            "Happiness of Countries Relative to their National Averages Over the Last Decade",
            anchor="middle",
        ),
    )
    .configure_view(stroke=None)
)

world_map

# %%
st.caption("")
st.write(
    """
Feel free to run the slider back and forth, observing the differences in global happiness over time. On the left are the happiness scores of each country, and on the right you can see how the differ from this countries mean score over all the years. Let's talk about some trends that we've noticed and what could have potentially led to these!
With the slider positioned at 2023/2024, it's fascinating (and a bit surprising) to observe that the eastern hemisphere has generally been seeing a rise in happiness scores. Perhaps cultural shifts towards mental health awareness, economic growth, and measures against societal discrimination are starting to bear fruit. 
Meanwhile, the western hemisphere tells a different story. There's a gradual decrease in happiness scores. This could perhaps be due to the political tensions, economic uncertainty, and a reckoning with systemic social issues that have swept this side of the planet. 
Looking at Africa, there isn't a coherent pattern. Some nations report significant spikes in happiness, while others face stagnation or decline. This lack of uniformity could be due to the diverse cultures, economies, and political landscapes present across the continent. Furthermore, data from some regions is often imperceptible, highlighting how infrequently these areas are surveyed.
A striking observation is that despite global ramifications from the Covid pandemic, the world has somewhat paradoxically seen an average increase in overall happiness scores since 2021! This apparent contradiction could perhaps be an embodiment of human resilience and adaptability in the face of adversity. 
As much as these charts reveal, they also uncover many more questions, provoking us to delve deeper into understanding the various hues of global happiness. 

One interesting thing to observe is that all the countries almost flip in color. Countries that were colored red in 2015 are now colored green, and vice versa. 
Middle Africa, China, and Eastern Europe seem to be doing better but the Americas, India and southern africa seem to be doing worse. Perhaps we can examine what changed and understand better.
But coming back to the initial hypothesis, money, social support and freedom are paramount to happiness but exactly how important these 3 things are compared to eachother is dependent on the culture of the people.
If we learnt one thing by decoding the report, it is that happiness can indeed be achieved by focusing on the governmental policies and setting priorities. It doesn't take long and a nation's history no matter what shouldn't deter it.
By focusing on improving the key areas mentioned before, nations can not only enhance the well-being and happiness of their citizens but also build more resilient and prosperous communities. This understanding is crucial for anyone aiming to foster a happier, more cohesive society, from government officials and policy-makers to community leaders and active citizens.
Have a happy day!"""
)
