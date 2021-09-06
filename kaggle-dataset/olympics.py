import pandas as pd
from collections import namedtuple, Counter
import matplotlib.pyplot as plt

# Load in the csv file
data = pd.read_csv('athlete_events.csv')
# Console display rows limit
pd.set_option('display.max_rows', 50)
# Pseudo return type for convenience of use in fetchUniqueWinners
UniqueWinners = namedtuple('UniqueWinners', ['Count','Set', 'WinnersList'])

# Fetch NOC-to-medals won per year & sort descendingly
# Output example:
#      NOC  Medal
# 198  USA    121
# 38   CHN     70
# 68   GBR     67
# 159  RUS     56
# 72   GER     42
# ..   ...    ...
# 94   IVB      0
# 100  KGZ      0
# 101  KIR      0
# 1    ALB      0
# 206  ZIM      0
# Returns dataframe for convenience
def fetchMedalsPerYear(year = "2016"):
    queryYearString = "Year == " + str(year)
    t = (
        data.query(queryYearString)
        .filter(["NOC", "Event", "Medal"])
        .groupby(["NOC", "Event"])
        .agg({"Medal": lambda x: x.nunique()})
        .groupby("NOC")
        .sum()
        .reset_index()
        .sort_values("Medal", ascending = False)
    )
    return t

# Fetch & build a list of unique NOCs in top n
# over the course of history
# Returns named tuple UniqueWinners
def fetchUniqueWinners(top = 3):
    eventYears = sorted(data.Year.unique().tolist())
    uniqueNOC = set()
    winnersList = []
    for year in eventYears:
        noc = fetchMedalsPerYear(year).head(top)["NOC"].tolist()
        winnersList.append(noc)
        uniqueNOC.update(noc)
    return UniqueWinners(len(uniqueNOC), uniqueNOC, winnersList)

def getWinnerFreq(winnderData):
    winnerFreq = Counter(item for sublist in winnerData.WinnersList for item in sublist)
    df = pd.DataFrame({'NOC': winnerFreq.keys(), 
                       'freq': winnerFreq.values()})
    df.set_index('NOC', inplace = True)
    df.sort_values('freq', inplace = True, ascending = False)
    return df


if __name__ == "__main__":
    # Get top 3 NOCs over the course of history
    winnerData = fetchUniqueWinners()
    print("Unique NOCs in top3: ", winnerData.Count)
    df = getWinnerFreq(winnerData)
    print("Frequency table of placing in top3")
    print(df)
    print("\n ------- \n")

    fig = df.plot(
                y = 'freq',
                title = 'Frequency of placing in Top 3 total medals 1896-2016',
                ylabel = 'Occurrences in top 3 [Count]',
                xlabel = 'NOC [National Olympic Committee]',
                kind = 'bar',
                legend = False
            )
    plt.tight_layout()
    fig.get_figure().savefig('plots/winnerFreqTop3.png')
    plt.close()
    # Get top 1 NOCs over the course of history
    winnerData = fetchUniqueWinners(1)
    print("Unique NOCs in top1:", winnerData.Count)
    df = getWinnerFreq(winnerData)
    print("Frequency table of placing in top1")
    print(df)
    fig = df.plot(
                y = 'freq',
                title = 'Frequency of placing in Top 1 total medals 1896-2016',
                ylabel = 'Occurrences in top 1 [Count]',
                xlabel = 'NOC [National Olympic Committee]',
                kind = 'bar',
                legend = False
            )
    plt.tight_layout()
    fig.get_figure().savefig('plots/winnerFreqTop1.png')
    plt.close()
    print("\n ------- \n")

    # Get top 10 countries by total medals in 2016
    print("2016 (most recent in the dataset) total medals data")
    df = fetchMedalsPerYear(2016)
    print(df.head(10))
    df = df.head(10)
    fig = df.plot(
                y = 'Medal',
                x = 'NOC',
                title = 'Total medals won in 2016 Olympic Games by country [Top 10]',
                ylabel = 'Total medals [Count]',
                xlabel = 'NOC [National Olympic Committee]',
                kind = 'bar',
                legend = False
            )
    plt.tight_layout()
    fig.get_figure().savefig('plots/top10Countries2016.png')
    plt.close()
    print("\n ------- \n")

    # Get total amount of medals per gender
    print("Total medals earned by gender 1896-2016")
    df = (
        data.filter(['Sex', 'Medal'])
        .groupby('Sex')
        .count()
        .reset_index()
    )
    print(df)
    fig = df.plot(
                y = 'Medal',
                x = 'Sex',
                title = 'Total medals earned by gender 1896-2016',
                ylabel = 'Total medals [Count]',
                xlabel = 'Gender',
                kind = 'bar',
                rot = 0,
                legend = False
            )
    plt.tight_layout()
    fig.get_figure().savefig('plots/totalMedalsByGender.png')
    plt.close()
    print("\n ------- \n")

    # Get medals by gender by year
    df = data.filter(['Year', 'Sex', 'Medal']).groupby(['Year', 'Sex']).count().reset_index()
    # Transpose gender column and keep medals as value
    df = df.pivot(index = 'Year', columns = 'Sex', values = 'Medal').fillna(0).reset_index()
    print(df)
    fig = df.plot(
                x = 'Year',
                y = ['M', 'F'],
                title = 'Total medals earned by gender by game 1896-2016',
                ylabel = 'Total medals [Count]',
                xlabel = 'Olympics [Year]',
                kind = 'bar',
                legend = True
            )
    plt.tight_layout()
    fig.get_figure().savefig('plots/medalsByGenderByGames.png')
    plt.close()
    print("\n ------- \n")

    # Get number of participants by year
    df = (
        data.filter(['Year', 'ID'])
        .groupby(['Year'])
        .agg({'ID': lambda x: x.nunique()})
        .reset_index()
    )

    print("Year - number of participants")
    print(df)
    fig = df.plot(
                x = 'Year',
                y = 'ID',
                title = 'Total athletes by year 1896-2016',
                ylabel = 'Participants [Count]',
                xlabel = 'Olympics [Year]',
                kind = 'bar',
                legend = False
            )
    plt.tight_layout()
    fig.get_figure().savefig('plots/participantsByYear.png')
    plt.close()
    print("\n ------- \n")

    # Get medal category by age
    df = data.query('Medal == Medal').filter(['Age', 'Medal'])

    fig = df.boxplot(
                by = 'Medal'
            )
    plt.tight_layout()
    plt.title('Age grouped by medal boxplot')
    fig.get_figure().savefig('plots/ageToMedal.png')
    plt.close()

    summary = (
        df.groupby('Medal')
        .describe()
        .unstack(1)
        .reset_index()
        .pivot(index = 'Medal', columns='level_1', values = 0)
    )
    df.groupby('Age').count()
    
    print("Basic statistical summary of medal groups by age")
    print(summary)
    print("\nTable of medals by age")
    df["value"] = 1
    df = df.pivot_table(index = 'Age', columns = 'Medal', values='value', aggfunc='count', fill_value=0).reset_index()
    #df = df.pivot(index = 'Age', columns = 'Medal')
    fig = df.plot(
                x = 'Age',
                y = ['Bronze', 'Silver', 'Gold'],
                color = ['brown', 'gray', 'yellow'],
                stacked = True,
                title = 'Medals by age 1896-2016',
                ylabel = 'Total medals [Count]',
                xlabel = 'Age',
                kind = 'bar',
                legend = True
            )
    plt.tight_layout()
    fig.get_figure().savefig('plots/medalsByAge.png')
    plt.close()
    print(df)
    print("\n ------- \n")

    # Get medal count by height
    df = (
        data.query('Medal == Medal')
        .filter(['Height', 'Medal'])
        .groupby('Height')
        .count()
        .reset_index()
    )

    print('Basic statistical summary of height historically')
    print(df['Height'].describe())
    print('\nMedals by height')
    print(df)

    plt.hist(df['Height'].tolist(), bins=30, weights=df['Medal'].tolist(), histtype='bar', ec='black')
    plt.plot()
    plt.title('Height-medal count histogram 1896-2016')
    plt.xlabel('Height [cm]')
    plt.ylabel('Total medals [Count]')
    
    plt.tight_layout()
    plt.savefig('plots/medalsByHeight.png')
    plt.close()
    print("\n ------- \n")

    # Get disciplines with highest ratio of short people (0-Q1)

    # Total amount of participants by sport
    dfAll = (
        data.filter(['Sport', 'ID'])
        .groupby('Sport')
        .agg({"ID" : lambda x: x.nunique()})
        .sort_values('ID', ascending = False)
    )
    # Total top10 amount of short participants by sport
    dfShort = (
        data.query('Height < 158')
        .filter(['Sport', 'ID'])
        .groupby('Sport')
        .agg({"ID": lambda x : x.nunique()})
        .sort_values('ID', ascending = False)
    )

    dfE = pd.merge(dfAll, dfShort, on = 'Sport', how = 'inner').reset_index()
    ratio = [y / x for x, y in zip(dfE['ID_x'], dfE['ID_y'])]
    dfE['ratio'] = ratio
    dfE['ratio'] = pd.to_numeric(dfE['ratio'], errors = 'coerce')
    dfE = dfE.sort_values('ratio', ascending = False)
    dfE = dfE.rename(columns = {
        'ID_x' : 'Total athletes',
        'ID_y' : 'Short athletes'
    }).head(10).sort_values('ratio')

    print('Top 10 sports in terms of short people participation ratio historically')
    print(dfE)
    
    fig = dfE.plot(
            x = 'Sport',
            y = ['Total athletes', 'Short athletes'],
            title = 'Top 10 sports by ratio of short people 1896-2016',
            ylabel = 'Total participants [Count]',
            xlabel = 'Sport',
            kind = 'barh',
            legend = True,
        )
    plt.tight_layout()
    fig.get_figure().savefig('plots/sportsByShortPeople.png')
    plt.close()
    print("\n ------- \n")

    # Get most popular surname among winners

    df = data.query('Medal == Medal').filter(['Name', 'ID']).drop_duplicates().groupby('ID').head(50)
    print('Example of name-id list, first 50 results')
    print(df)
    print("\n")
    names = df['Name'].tolist()
    surnames = []
    for name in names:
        # Split name string into words
        tName = name.split(" ")
        # Check if last word starts with (, ie. Galina Ivanovna Zybina (-Fyodorova) 
        # if so, we treat the second last word as surname
        # Is III a valid surname?
        if(tName[-1] == '' or tName[-1][0] == '(' or
           tName[-1] == 'Jr.' or tName[-1] == 'Sr.' or
           tName[-1] == "III"):
            surnames.append(tName[-2])
        else:
            surnames.append(tName[-1])
    
    surnames = Counter(surnames)
    name, count = zip(*surnames.most_common(20))

    df = pd.DataFrame({
        'Name' : name,
        'Count': count
    }).sort_values('Count')

    fig = df.plot(
            x = 'Name',
            y = 'Count',
            title = 'Frequency of common surnames among medalists 1896-2016',
            ylabel = 'Occurrences [Count]',
            xlabel = 'Surname',
            kind = 'barh',
            legend = False
        )
    plt.tight_layout()
    fig.get_figure().savefig('plots/winnerSurnameFreq.png')
    plt.close()


        


    






