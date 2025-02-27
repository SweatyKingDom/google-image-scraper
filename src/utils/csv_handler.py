import csv

def read_search_queries(csv_file):
    queries = []
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                queries.append({
                    'query': row['query'],
                    'alt_text': row['alt_text']
                })
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
    return queries

def write_results_to_csv(results, csv_file):
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['index', 'span_text', 'alt_text']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                writer.writerow(row)
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier CSV : {e}")