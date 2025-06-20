import pandas as pd
import ast

def getSmallDescriptions():
    df = pd.read_csv("final.csv")
    
    small_descriptions = df[df['Description'].str.split().str.len() < 30]
    #Print the lines with less than 30 words
    #print(small_descriptions)

    #return csv file with the lines with less than 30 words
    #small_descriptions.to_csv("small_descriptions.csv", index=False)
    
    return len(small_descriptions)

#print(getSmallDescriptions())

def cleanNullParticipants():
    df = pd.read_csv("final.csv")

    dfFiltered = df[(df['Winner'] == 'Massacre') | (df['Winner'] == 'Draw') | (df['Winner'] == 'Accidental incident') | (df['Winner'] == 'Incident')]
    dfFiltered.loc[dfFiltered['Participants'].isnull(), 'Participants'] = "[]"

    df.update(dfFiltered)
    print(df[df['Participants'].isnull()]['ID'])

    """
    df.loc[df['Participants'].isnull(), 'Participants'] = df.apply(
        lambda row: [row['Winner'], row['Loser']] if pd.notnull(row['Winner']) and pd.notnull(row['Loser']) else [], axis=1
    )
    """

    df.loc[df['Participants'].isnull(), 'Participants'] = df.apply(
        lambda row: (
            [name.strip() for name in str(row['Winner']).split(',')] + 
            [name.strip() for name in str(row['Loser']).split(',')]
        ) if pd.notnull(row['Winner']) and pd.notnull(row['Loser']) else [], 
        axis=1
    )

    #print(df['Participants'].isnull().sum())


    df.to_csv("final.csv", index=False)

#cleanNullParticipants()

def cleanEmptyParticipants():
    df = pd.read_csv("final.csv")

    print(df[df['Participants'] == "[]"]['ID'])

    df.loc[df['Participants'] == "[]", 'Participants'] = df.apply(
        lambda row: (
            [name.strip() for name in str(row['Winner']).split(',')] + 
            [name.strip() for name in str(row['Loser']).split(',')]
        ) if pd.notnull(row['Winner']) and pd.notnull(row['Loser']) else [], 
        axis=1
    )

    df.to_csv("final.csv", index=False)

#cleanEmptyParticipants()

def cleanDuplicatesParticipants():
    df = pd.read_csv("final.csv")

    def parse_and_clean(entry):
        try:
            # Attempt to convert the string to a list
            items = ast.literal_eval(entry)
            if isinstance(items, list):
                # Remove duplicates and sort if it's a list
                return list(sorted(set(items)))
        except (ValueError, SyntaxError):
            # If parsing fails, return the original entry
            return entry
        
    df['Participants'] = df['Participants'].apply(parse_and_clean)
    
    df.to_csv("final.csv", index=False)

#cleanDuplicatesParticipants()

def dropColumns():
    df = df = pd.read_csv("final.csv")

    columns_to_drop = ['Page']

    df = df.drop(columns=columns_to_drop)
    df.to_csv("final.csv", index=False)

dropColumns()

