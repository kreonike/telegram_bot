#@title **Setup Environment**

import subprocess, time
print("Setting up environment...")
start_time = time.time()
all_process = [
    ['pip', 'install', 'torch==1.12.1+cu113', 'torchvision==0.13.1+cu113', '--extra-index-url', 'https://download.pytorch.org/whl/cu113'],
    ['pip', 'install', '-U', 'sentence-transformers'],
    ['pip', 'install', 'httpx'],
]
for process in all_process:
    running = subprocess.run(process,stdout=subprocess.PIPE).stdout.decode('utf-8')

end_time = time.time()
print(f"Environment set up in {end_time-start_time:.0f} seconds")



#@title **Define Mubert methods and pre-compute things**

import numpy as np
from sentence_transformers import SentenceTransformer
minilm = SentenceTransformer('all-MiniLM-L6-v2')

mubert_tags_string = 'tribal,action,kids,neo-classic,run 130,pumped,jazz / funk,ethnic,dubtechno,reggae,acid jazz,liquidfunk,funk,witch house,tech house,underground,artists,mystical,disco,sensorium,r&b,agender,psychedelic trance / psytrance,peaceful,run 140,piano,run 160,setting,meditation,christmas,ambient,horror,cinematic,electro house,idm,bass,minimal,underscore,drums,glitchy,beautiful,technology,tribal house,country pop,jazz & funk,documentary,space,classical,valentines,chillstep,experimental,trap,new jack swing,drama,post-rock,tense,corporate,neutral,happy,analog,funky,spiritual,sberzvuk special,chill hop,dramatic,catchy,holidays,fitness 90,optimistic,orchestra,acid techno,energizing,romantic,minimal house,breaks,hyper pop,warm up,dreamy,dark,urban,microfunk,dub,nu disco,vogue,keys,hardcore,aggressive,indie,electro funk,beauty,relaxing,trance,pop,hiphop,soft,acoustic,chillrave / ethno-house,deep techno,angry,dance,fun,dubstep,tropical,latin pop,heroic,world music,inspirational,uplifting,atmosphere,art,epic,advertising,chillout,scary,spooky,slow ballad,saxophone,summer,erotic,jazzy,energy 100,kara mar,xmas,atmospheric,indie pop,hip-hop,yoga,reggaeton,lounge,travel,running,folk,chillrave & ethno-house,detective,darkambient,chill,fantasy,minimal techno,special,night,tropical house,downtempo,lullaby,meditative,upbeat,glitch hop,fitness,neurofunk,sexual,indie rock,future pop,jazz,cyberpunk,melancholic,happy hardcore,family / kids,synths,electric guitar,comedy,psychedelic trance & psytrance,edm,psychedelic rock,calm,zen,bells,podcast,melodic house,ethnic percussion,nature,heavy,bassline,indie dance,techno,drumnbass,synth pop,vaporwave,sad,8-bit,chillgressive,deep,orchestral,futuristic,hardtechno,nostalgic,big room,sci-fi,tutorial,joyful,pads,minimal 170,drill,ethnic 108,amusing,sleepy ambient,psychill,italo disco,lofi,house,acoustic guitar,bassline house,rock,k-pop,synthwave,deep house,electronica,gabber,nightlife,sport & fitness,road trip,celebration,electro,disco house,electronic'
mubert_tags = np.array(mubert_tags_string.split(','))
mubert_tags_embeddings = minilm.encode(mubert_tags)

from IPython.display import Audio, display
import httpx
import json

def get_track_by_tags(tags, pat, duration, maxit=20, autoplay=False, loop=False):
  if loop:
    mode = "loop"
  else:
    mode = "track"
  r = httpx.post('https://api-b2b.mubert.com/v2/RecordTrackTTM',
      json={
          "method":"RecordTrackTTM",
          "params": {
              "pat": pat,
              "duration": duration,
              "tags": tags,
              "mode": mode
          }
      })

  rdata = json.loads(r.text)
  assert rdata['status'] == 1, rdata['error']['text']
  trackurl = rdata['data']['tasks'][0]['download_link']

  print('Generating track ', end='')
  for i in range(maxit):
      r = httpx.get(trackurl)
      print(r)
      if r.status_code == 200:
          display(Audio(trackurl, autoplay=autoplay))
          break
      time.sleep(1)
      print('.', end='')

def find_similar(em, embeddings, method='cosine'):
    scores = []
    for ref in embeddings:
        if method == 'cosine':
            scores.append(1 - np.dot(ref, em)/(np.linalg.norm(ref)*np.linalg.norm(em)))
        if method == 'norm':
            scores.append(np.linalg.norm(ref - em))
    return np.array(scores), np.argsort(scores)

def get_tags_for_prompts(prompts, top_n=3, debug=False):
    prompts_embeddings = minilm.encode(prompts)
    ret = []
    for i, pe in enumerate(prompts_embeddings):
        scores, idxs = find_similar(pe, mubert_tags_embeddings)
        top_tags = mubert_tags[idxs[:top_n]]
        top_prob = 1 - scores[idxs[:top_n]]
        if debug:
            print(f"Prompt: {prompts[i]}\nTags: {', '.join(top_tags)}\nScores: {top_prob}\n\n\n")
        ret.append((prompts[i], list(top_tags)))
    return ret

#@markdown **Get personal access token in Mubert and define API methods**
email = "kreonike@gmail.com" #@param {type:"string"}

r = httpx.post('https://api-b2b.mubert.com/v2/GetServiceAccess',
    json={
        "method":"GetServiceAccess",
        "params": {
            "email": email,
            "license":"ttmmubertlicense#f0acYBenRcfeFpNT4wpYGaTQIyDI4mJGv5MfIhBFz97NXDwDNFHmMRsBSzmGsJwbTpP1A6i07AXcIeAHo5",
            "token":"4951f6428e83172a4f39de05d5b3ab10d58560b8",
            "mode": "loop"
        }
    })

rdata = json.loads(r.text)
assert rdata['status'] == 1, "probably incorrect e-mail"
pat = rdata['data']['pat']
print(f'Got token: {pat}')



duration = 60

prompts = [
    'kind beaver guards life tree, stan lee, epic'
]

tags = get_tags_for_prompts(prompts)

for i, tag in enumerate(tags):
  print(f'Prompt: {tag[0]}\nTags: {tag[1]}')
  try:
    get_track_by_tags(tag[1], pat, duration, autoplay=False)
  except Exception as e:
    print(str(e))
  print('\n')



