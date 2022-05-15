from flask import Flask, render_template, jsonify, request, redirect, url_for
import pickle

from backend import searchdocument,textsummarize,textclassify,entityrecognition,texttospeech, speechrecognition

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/modal')
def modal():
    return render_template('modal.html')

@app.route('/default')
def default():
    return render_template('default.html')
    

@app.route('/search',methods=['GET'])
def searchpage():
    
    search_text = request.args["search"]

    results = searchdocument.search_doc(search_text)
    summary_list, classify_list , entity_list , keyphrase_list, location_list = [], [], [], [], []
    content_dict = {}
    result_dict = {}
    for result in results:
        summary = textsummarize.get_summary([result['content']])
        summary_list.append(summary)
        classified_label = textclassify.sample_classify_document_single_category([result['content']])
        classify_list.append(classified_label)

        entity = entityrecognition.sample_recognize_custom_entities([result['content']])
        entity_list.append(entity)
        keyphrase_list.append(result['keyphrases'][:5])
        location_list.append(result['locations'])
        content_dict[entity[0]] = result['content']
        result_dict[result['metadata_storage_name']] = {'content': result['content'],
                                                        'people': result['people'],                                                       
                                                       'organizations': result['organizations'],
                                                       'locations': result['locations'],
                                                       'summary': summary,
                                                       'class': classified_label,
                                                       'entities': entity[0],
                                                       'keyphrases': result['keyphrases'][:5]
                                                       }

    with open('data/results.pkl','wb') as f:
        pickle.dump(result_dict, f, pickle.HIGHEST_PROTOCOL)
       

    # pickle.dump(content_list,'data/contents.pkl')
    with open('data/contents.pkl', 'wb') as f:
        pickle.dump(content_dict, f, pickle.HIGHEST_PROTOCOL)
    
    return render_template('search.html',
                            search_results=zip(summary_list,classify_list,entity_list,keyphrase_list), 
                            query_results = results,
                            search_terms=search_text,
                            )

@app.route('/refined_result',methods=['GET', 'POST'])
def refined_result():

    with open('data/results.pkl', 'rb') as f:
        results = pickle.load(f)

    summary_list,classify_list, entity_list,keyphrase_list = [],[],[],[]
    for key in results.keys():
        summary_list.append(key['summary'])
        classify_list.append(key['class'])
        keyphrase_list.append(key['keyphrases'])

    return render_template('refine_result.html', search_results=zip(summary_list,classify_list,entity_list,keyphrase_list))


@app.route('/filter_data',methods=['GET', 'POST'])
def filter_data():

    location = '' if not request.args.get("locations") else request.args.get("locations")
    org = '' if not request.args.get("organizations") else request.args.get("organizations")
    people = '' if not request.args.get("people") else request.args.get("people")
    category  = '' if not request.args.get("class") else request.args.get("class")

    with open('data/results.pkl', 'rb') as f:
        results = pickle.load(f)

    filtered = {}
    for key in results.keys():
        if location in results[key]['locations']\
             or org in results[key]['organizations']\
             or people in results[key]['people']\
             or category in results[key]['class']:
            filtered[key] = results[key]

    summary_list,classify_list, entity_list,keyphrase_list = [],[],[],[]
    for key in filtered.keys():
        value = filtered[key]
        summary_list.append(value['summary'])
        classify_list.append(value['class'])
        keyphrase_list.append(value['keyphrases'])
        entity_list.append(value['entities'])

    return render_template('refine_result.html', filtered_data = zip(summary_list,classify_list, entity_list,keyphrase_list))


@app.route('/fullarticle',methods=['GET', 'POST'])
def fullarticle():

    title = request.args['title']
    

    # content_list = pickle.load('data/contents.pkl')
    with open('data/contents.pkl', 'rb') as f:
        content_list = pickle.load(f)
    # print(content_list)
    return render_template('fullarticle.html', content=content_list,index=title)


@app.route('/speak',methods=['GET', 'POST'])
def speak():

    article = request.args['article']
    title = request.args['title']
    
    texttospeech.text_to_speech(article)

    with open('data/contents.pkl', 'rb') as f:
        content_list = pickle.load(f)

    return render_template('fullarticle.html', content=content_list, index=title)
    # return redirect(url_for('speak'))

@app.route('/speak_detail',methods=['GET', 'POST'])
def speak_detail():

    with open('data/results.pkl', 'rb') as f:
        results = pickle.load(f) 

    texttospeech.text_to_speech("{} articles found.".format(len(results.keys())))

    for i,key in enumerate(results.keys()):
        value = results[key]
        title = value['entities']
        summary = value['summary']
        category = value['class'][0]
        score = value['class'][1]
        text = "Article {}. Title. {}. Summary. {}. Classified as {} with {} confidence.".format(str(i+1),
                                                                                                title,
                                                                                                summary,
                                                                                                category,
                                                                                                score
                                                                                            )
    
        texttospeech.text_to_speech(text)
        texttospeech.text_to_speech("Reading Completed. Returning to search")


    return render_template('default.html')
    


    

@app.route('/voice_search',methods=['GET', 'POST'])
def voice_search():

    texttospeech.text_to_speech("Speak you search word into your microphone")
    
    text = speechrecognition.recognize_from_microphone()

    texttospeech.text_to_speech("recognized word" +text+"Click Enter to Search")

    return render_template('default.html', recognized_text=text)

    

    
    
@app.route('/help')
def help():

    helptext = 'Hi I am your AI Professor. You can use short cut keys. To Search . Alt plus s and spell the word and click enter. to read article alt plus r . to hear the help voice . alt plus h'
    
    texttospeech.text_to_speech(helptext)

    return render_template('default.html')
    # return redirect(url_for('speak'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)