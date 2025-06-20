import pandas as pd
import wikipediaapi
import requests
from bs4 import BeautifulSoup

# ---------------------- WIKIPEDIA API ----------------------

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='ProjectName/1.0 (email@example.com)'
)

# Search the description with the API of Wikipedia
def get_battle_description_wikipedia(battle_name,battle_year,current_description):
    # Search for the battle name with "Battle of" prefix
    search_name = f"Battle of {battle_name} ({battle_year})"
    page = wiki_wiki.page(search_name)
    if page.exists():
        # Split the summary into paragraphs
        paragraphs = page.summary.split('\n')
        # Return the first and second paragraph if it exists
        if len(paragraphs) > 1:
            print("Encontrei a batalha com 2 parágrafos - ", search_name)
            return paragraphs[0] + " " + paragraphs[1]
        else:
            return paragraphs[0] if paragraphs else current_description
    else:
        return current_description

def get_battle_description_wikipedia_siege(battle_name,battle_year):
    # Search for the battle name with "Battle of" prefix
    format_battle = battle_year
    if isinstance(battle_year, str) and battle_year.startswith('-'):
        format_battle = format_battle_name_BC(battle_year)

    search_name = f"Siege of {battle_name} {format_battle}"
    page = wiki_wiki.page(search_name)
    if page.exists():
        # Split the summary into paragraphs
        paragraphs = page.summary.split('\n')
        # Return the first paragraph
        return paragraphs[0] if paragraphs else "No description available"
    else:
        return "No description available" 

def get_battle_description_wikipedia_short(battle_name, battle_year, current_description):
    # Convert the year to a string for comparison.
    battle_year = str(battle_year) if battle_year else None

    # Search for the battle name with "Battle of" prefix.
    search_name = f"Siege of {battle_name}"
    page = wiki_wiki.page(search_name)
    
    if page.exists():
        # Check if the page is a disambiguation page by looking for certain phrases.
        if "may refer to" in page.summary or len(page.links) > 1:

            disambiguation_url = page.fullurl
            response = requests.get(disambiguation_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all links on the disambiguation page.
                links = soup.find_all('a', href=True)

                for link in links:
                    if battle_name and battle_year in link.get_text():
                        print(link.get_text())
                        specific_page = wiki_wiki.page(link.get_text())
                        if specific_page.exists():
                            print("Encontrei a batalha")
                            # Return the first paragraph from the specific battle page.
                            paragraphs = specific_page.summary.split('\n')
                            # Return the first and second paragraph if it exists
                            if len(paragraphs) > 1:
                                print("Encontrei a batalha com 2 parágrafos")
                                return paragraphs[0] + " " + paragraphs[1]
                            else:
                                return paragraphs[0] if paragraphs else current_description
                        else:
                            print("Não encontrei a batalha")
                return current_description
        else:
            return current_description
    else:
        return current_description


def get_battle_description_wikipedia_2_paragraphs(battle_name,battle_year,current_description):
    search_name = f"Battle of {battle_name} ({battle_year})"
    print(search_name)
    page = wiki_wiki.page(search_name)
    if page.exists():
        print("Page exists")
        paragraphs = page.summary.split('\n')
        print(paragraphs)
        if len(paragraphs) > 1:
            return paragraphs[0] + " " + paragraphs[1]
        elif len(paragraphs) == 1:
            return paragraphs[0]
        else:
            return current_description
    else:
        print("Page does not exist")
        return

def format_battle_name_BC(battle_year):
    int_year = int(battle_year)
    if int_year < 0:
        return f"{abs(int_year)} BC"




# ---------------------- 10000BATTLES API ----------------------

def get_battle_list():
    url = "https://www.10000battles.com/battles2.php?bat=6"  # URL example
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the dropdown list
        dropdown = soup.find('select', {'name': 'menus'}) 
        options = dropdown.find_all('option')
        
        # Create a dictionary with the battle names and their respective IDs
        battle_names = {option.text.strip(): option['value'] for option in options if 'value' in option.attrs and option['value']}
        return battle_names
    else:
        return {}


# Format the ID of the dataset to match the website dropdown list
def format_battle_name(battle_name):
    for i, char in enumerate(battle_name):
        if char.isdigit() or (char == '-' and i+1 < len(battle_name) and battle_name[i+1].isdigit()):
            return f"{battle_name[:i].strip()}, {battle_name[i:].strip()}"
    return battle_name


# Get the URL of the battle from the list
def get_battle_url_from_list(battle_name, battle_list):
    formatted_name = format_battle_name(battle_name)
    for battle, url in battle_list.items():
        if formatted_name in battle:
            return url
    return None

# Get the description from the 10000battles website
def get_battle_description_10000battles(battle_url):
    url = f"https://www.10000battles.com/{battle_url}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the description
        description = soup.find('div', class_='inf_r').text.strip()
        
        # Replace newlines with spaces
        description = description.replace('\n', ' ')

        return description if description else "No description found"
    else:
        return "Failed to retrieve page"


# ---------------------- MAIN ----------------------

# Output the dataset with the descriptions using the 2 APIs 
def output_dataset(df, battle_list):
    def get_combined_description(row):
        description = get_battle_description_wikipedia(row['Battle'])
        if description == "No description available":
            battle_url = get_battle_url_from_list(row['ID'], battle_list)
            if battle_url:
                return get_battle_description_10000battles(battle_url)
        return description
    
    df['Description'] = df.apply(get_combined_description, axis=1)
    return df

# Update the missing descriptions using Wikipedia
def update_missing_descriptions_with_siege(df):
    missing_description_df = df[df['Description'] == "No description available"].copy()

    missing_description_df['Description'] = missing_description_df.apply(
        lambda row: get_battle_description_wikipedia_siege(row['Battle'],row['Year']),
        axis=1
    )
    
    df.update(missing_description_df)
    
    return df

# Update the ambiguous descriptions using Wikipedia
def update_ambiguous_descriptions(df):
    # Use 'na=False' to safely handle NaN values in the 'Description' column.
    #ambiguous_desc_df = df[df['Description'].str.endswith("to:", na=False)]

    # Filter for descriptions that has "may refer to"
    ambiguous_desc_df = df[df['Description'].str.contains("may refer to", na=False)]

    # Update the descriptions using .loc to avoid SettingWithCopyWarning.
    df.loc[ambiguous_desc_df.index, 'Description'] = ambiguous_desc_df.apply(
        lambda row: get_battle_description_wikipedia_short(row['Battle'], row['Year'], row['Description']),
        axis=1
    )
    
    # Return the modified DataFrame.
    return df

# Update the missing descriptions using 10000battles
def update_missing_descriptions(df, battle_list):
    def get_description(row):
        battle_url = get_battle_url_from_list(row['ID'], battle_list)
        if battle_url:
            return get_battle_description_10000battles(battle_url)
        
        return row['Description']

    missing_description_df = df[df['Description'] == "No description available"].copy()

    missing_description_df['Description'] = missing_description_df.apply(get_description, axis=1)

    df.update(missing_description_df)

    return df

# Update descriptions with less than 30 words using 10000battles
def update_short_descriptions_10000battles(df, battle_list):
    # Filter for descriptions with less than 30 words
    short_desc_df = df[df['Description'].str.split().str.len() < 30].copy()

    # Function to get description from 10000battles
    def get_description(row):
        battle_url = get_battle_url_from_list(row['ID'], battle_list)
        if battle_url:
            print("Encontrei a batalha")
            return get_battle_description_10000battles(battle_url)
        else:
            print("Não encontrei a batalha")
        
        return row['Description']

    # Apply the description update function
    short_desc_df['Description'] = short_desc_df.apply(get_description, axis=1)

    # Update the original dataframe with the new descriptions
    df.update(short_desc_df)

    return df


#Update descriptions with less than 30 words using Wikipedia
def update_short_descriptions_wikipedia(df):
    short_desc_df = df[df['Description'].str.split().str.len() < 30].copy()

    def get_description(row):
        return get_battle_description_wikipedia(row['Battle'],row['Year'],row['Description'])

    short_desc_df['Description'] = short_desc_df.apply(get_description, axis=1)

    df.update(short_desc_df)

    return df

#---------------------- DROP ROWS ----------------------
def drop_rows(df):
    # Remove rows where the 'Description' is "No description available"
    df = df[df['Description'] != "No description available"]

    # Drop rows where 'Description' ends with "to:", but first ensure there are no NaN values
    df = df[~df['Description'].fillna("").str.endswith("to:")]

    return df

# ---------------------- EXAMPLE USAGE ----------------------

df = pd.read_csv("final.csv")

# Apply the 10000battles description update to rows with less than 30 words
#battle_list = get_battle_list()
#df = update_short_descriptions_10000battles(df, battle_list)

# Apply the wikipedia description update to rows with less than 30 words
#df = update_short_descriptions_wikipedia(df)

# Apply the drop rows function
#df = drop_rows(df)

# Apply for ambiguous descriptions
df = update_ambiguous_descriptions(df)

# Apply the "Siege of" description update to rows with missing descriptions
#df = update_missing_descriptions_with_siege(df)

# Apply the 10000battles description update to rows with missing descriptions
#battle_list = get_battle_list()
#df = update_missing_descriptions(df,battle_list)

# Save the resulting dataset
df.to_csv("final_test.csv", index=False)

