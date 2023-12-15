import spacy
from spacy.matcher import Matcher
import psycopg2

city_labels = {
    'New York': 'NY54',
    'Cambridge': 'CMBR',
    'Chicago': 'CHCG',
    'Cleveland': 'CLEV',
    'Raleigh': 'RLGH',
    'Atlanta': 'ATLN',
    'Philadelphia': 'PHLA',
    'Washington': 'WASH',
    'Nashville': 'NSVL',
    'St. Louis': 'STLS',
    'New Orleans': 'NWOR',
    'Houston': 'HSTN',
    'San Antonio': 'SNAN',
    'Dallas': 'DLLS',
    'Orlando': 'ORLD',
    'Denver': 'DNVR',
    'Kansas City': 'KSCY',
    'San Francisco': 'SNFN',
    'Sacramento': 'SCRM',
    'Portland': 'PTLD',
    'Seattle': 'STTL',
    'Salt Lake City': 'SLKC',
    'Los Angeles': 'LA03',
    'San Diego': 'SNDG',
    'Phoenix': 'PHNX'
}


nlp = spacy.load("en_core_web_sm")

def extract_info_based_on_keywords(doc):
    matcher = Matcher(nlp.vocab)

    # patterns to match the keywords followed by one or more proper nouns
    patterns = [
        [{"LOWER": "to"}, {"POS": "PROPN", "OP": "+"}],
        [{"LOWER": "from"}, {"POS": "PROPN", "OP": "+"}],
        [{"LOWER": "through"}, {"POS": "PROPN", "OP": "+"}]
    ]

    # adding patterns to the matcher
    for pattern in patterns:
        matcher.add("KeyPhrases", [pattern])

    info = {}

    # using named entity recognition to find organizations
    for ent in doc.ents:
        if ent.label_ == "ORG":
            info['organization'] = ent.text
            
    # matching patterns for source, destination, and middle hop
    for match_id, start, end in matcher(doc):
        key = doc[start].text.lower()
        value = doc[start + 1:end].text  # capture all tokens after the keyword until the pattern ends

        if key == 'to':
            info['destination'] = value
        elif key == 'from':
            info['source'] = value
        elif key == 'through':
            info['middle_hop'] = value

    return info

def generate_query(info):
    queries = {
        'traffic_handling': """
            SELECT f.*, n1.label AS source_label, n2.label AS target_label, e.link_label
            FROM flows f
            JOIN nodes n1 ON f.path LIKE n1.id || ' -> %' OR f.path LIKE '% -> ' || n1.id || ' -> %'
            JOIN nodes n2 ON f.path LIKE '% -> ' || n2.id
            JOIN edges e ON (e.source = n1.id AND e.target = n2.id) OR (e.source = n2.id AND e.target = n1.id)
            WHERE f.organization LIKE '%{}%';
        """,
        'traffic_through': """
            WITH target_org_flows AS (
                SELECT f.*
                FROM flows f
                WHERE f.organization LIKE '%{}%' -- target organization
                AND f.path LIKE CONCAT('% -> ', (SELECT id FROM nodes WHERE label = '{}')) --  target exit city
            ),
            deviation_flows AS (
                SELECT f.*
                FROM target_org_flows f
                WHERE f.path NOT LIKE CONCAT('%',(SELECT id FROM nodes WHERE label = '{}'), '%') -- Replace with the city to check in the path
            )
            SELECT
                CASE
                    WHEN COUNT(*) = 0 THEN CONCAT('Yes, all traffic exiting in ', '{}', ' from ', '{}', ' passes through ', '{}')
                    ELSE CONCAT('No, not all traffic exiting in ', '{}', ' from ', '{}', ' passes through ', '{}', '. Deviations found from the following sources: ', STRING_AGG(DISTINCT source_label, ', '))
                END as traffic_summary
            FROM (
                SELECT f.*, n.label as source_label
                FROM deviation_flows f
                JOIN nodes n ON f.path LIKE CONCAT(n.id, ' -> %')
            ) as deviations;
        """,
        'multiple_egresses': """
            SELECT
                f.organization,
                STRING_AGG(DISTINCT n.label, ', ') AS egress_points
            FROM
                flows f
            JOIN
                nodes n ON f.path LIKE CONCAT('% -> ', n.id)
            GROUP BY
                f.organization
            HAVING
                COUNT(DISTINCT n.id) > 1; 
        """
    }
    
    # replacing city names in info with their corresponding labels
    for key in ['destination', 'middle_hop', 'source']:
        if key in info and info[key] in city_labels:
            info[key] = city_labels[info[key]]

    
    # choose which query to use
    if 'organization' in info and 'destination' in info and 'middle_hop' in info:
        query_template = queries['traffic_through']
        query = query_template.format(info['organization'], info['destination'], info['middle_hop'], info['destination'], info['organization'], info['middle_hop'], info['destination'], info['organization'], info['middle_hop'])
    elif 'organization' in info:
        query_template = queries['traffic_handling']
        query = query_template.format(info['organization'])
    else:
        query = queries['multiple_egresses']

    return query


def execute_query(query):
    # Database connection details
    db_name = "net2text" 
    db_user = "postgres" #change with your username
    db_pwd = "password"  # change with your password
    db_host = "localhost" 
    db_port = "5433"

    conn = psycopg2.connect(
        database=db_name, 
        user=db_user, 
        password=db_pwd,
        host=db_host, 
        port=db_port
    )


    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()

  
    cursor.close()
    conn.close()

    return records

def main():
   
    user_query = input("Enter your query: ")

    doc = nlp(user_query)
    info = extract_info_based_on_keywords(doc)
    sql_query = generate_query(info)

    records = execute_query(sql_query)
    for record in records:
        print(record)

if __name__ == "__main__":
    main()
