import csv
import json
import subprocess

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/parse', methods=['GET'])
def parse_url():

  with open('result.csv', 'w') as csvfile:
    pass

  with open('data.json', 'w') as file:
    pass

  url = request.args.get('url')
  if url:
    process = subprocess.Popen(['python', 'ANDRX_NGU_parser.py', url], stdout=subprocess.PIPE)
    process.communicate()
    return_code = process.wait()

    if return_code == 0:
      parse = []
      fl = True

      page = ''
      page_title = ''
      page_url = ''
      letters_count = ''
      numbers_count = ''

      with open('result.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
          if len(row) == 5:
            if fl:
              page, page_title, page_url, letters_count, numbers_count = row
              fl = False
            else:
              a, b, c, d, e = row
              parse.append({page : int(a), page_title : b, page_url: c, letters_count : int(d), numbers_count: int(e)})

      with open('data.json', 'w') as file:
        file.write(json.dumps({f'parse {url}': parse}))

      return jsonify({f'parse {url}': parse})
    
    else:
      with open('data.json', 'w') as file:
        file.write(json.dumps({'error': 'Bad URL parameter for parser'}))

      return jsonify({'error': 'Bad URL parameter for parser'})
    
  
  with open('data.json', 'w') as file:
      file.write(json.dumps({'error': 'Wrong URL parameter'}))

  return jsonify({'error': 'Wrong URL parameter'})

if __name__ == '__main__':
  app.run(debug=True)