import re
import json
from datetime import datetime

def sync_buildstate(md_file, json_file):
    # Read Markdown file
    with open(md_file, 'r') as f:
        md_content = f.read()

    # Load existing JSON
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    # Extract features from Feature Requirements Table
    feature_pattern = re.compile(r'\| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|', re.MULTILINE)
    features = []
    for match in feature_pattern.finditer(md_content):
        features.append({
            'id': match.group(1).strip(),
            'name': match.group(2).strip(),
            'priority': match.group(3).strip(),
            'status': match.group(4).strip(),
            'desc': match.group(5).strip()
        })

    # Extract bugs from Known Issues section
    bug_pattern = re.compile(r'- \*\*([^:]+):**\s*([^\n]+)', re.MULTILINE)
    bugs = [{'id': match.group(1).lower().replace(' ', '_'), 'desc': match.group(2).strip()} for match in bug_pattern.finditer(md_content)]

    # Extract next steps from Roadmap section
    next_pattern = re.compile(r'\d+\.\s*\*\*([^\n]+)**', re.MULTILINE)
    next_steps = [match.group(1).strip() for match in next_pattern.finditer(md_content)]

    # Extract decisions from Change Log
    decision_pattern = re.compile(r'- \*\*(\d{4}-\d{2}-\d{2}) \| v\d+\.\d+ \| ([^\n]+)**', re.MULTILINE)
    decisions = [{'date': match.group(1), 'type': 'unknown', 'desc': match.group(2).strip()} for match in decision_pattern.finditer(md_content)]

    # Update JSON data
    json_data['features'] = features
    json_data['bugs'] = bugs
    json_data['next_steps'] = next_steps
    json_data['decisions'] = decisions
    json_data['change_log'].append({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'version': json_data['meta']['spec'],
        'desc': f'Synced features, bugs, next steps, and decisions from {md_file}',
        'synced_with': md_file
    })
    json_data['meta']['rebalanced_at'] = datetime.now().strftime('%Y-%m-%d')

    # Save updated JSON
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)

    print(f'Synced {md_file} to {json_file}')

if __name__ == '__main__':
    sync_buildstate('buildstate.md', 'buildstate.json')