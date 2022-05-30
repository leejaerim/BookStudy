import csv
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template,request,redirect,send_file

def save_to_file(jobs:list)->None:
  #fn = fn.replace("/","_")
  with open("jobs.csv", mode="w") as file:
      writer = csv.writer(file)
      writer.writerow(["title", "company", "location", "link"])
      for job in jobs:
        writer.writerow(list(job.values()))

def get_jobs(word)->list:
  return wwr_get_jobs(word)+rem_get_jobs(word)
  # -----------------------------------------------------------------------

def wwr_get_jobs(word)->list:
  result = []
  url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={word}"
  site = requests.get(url)
  soup = BeautifulSoup(site.text,"html.parser")
  section = soup.find_all("section",{"class":"jobs"})
  for i in section:
    list = i.find_all("li")
    for j in list:
      target = j.find("a",recursive=False)
      link = target["href"]
      title = target.find("span",{"class":"title"})
      company = target.find("span",{"class":"company"})
      location = target.find("span",{"class":"region company"})
      if title is not None and company is not None and location is not None :
        result.append({
        'title' : title.get_text(strip=True),'company' : company.get_text(strip=True),'location' : location.get_text(strip=True),'link' : "https://weworkremotely.com/"+link
        })
  return result

def rem_get_jobs(word)->list:
  result = []
  url = f"https://remoteok.com/remote-{word}-jobs"
  site = requests.get(url)
  soup = BeautifulSoup(site.text,"html.parser")
  table = soup.find("table",{"id":"jobsboard"})
  if table is not None :
    jobs = table.find("tbody").find_all("tr",{"class":"job"})
    for i in jobs:
      target = i.find("td",{"class","company"})
      title = target.find("a")
      company = target.find("span")
      link = target.find("a")["href"]
      location = target.find("div",{"class":"location"})
      if title is not None and company is not None and location is not None :
        result.append({
        'title' : title.get_text(strip=True),'company' : company.get_text(strip=True),'location' : location.get_text(strip=True),'link' : "https://weworkremotely.com/"+link
        })
  return result




#스택오버플로우컴퍼니가 서비스 종료함에 따라 REMOTEOK와 weworkremotely.com 두 사이트를 스크래핑함.
#또, REMOTEOK의 경우, 잦은 호출로 인한 503 에러가 뜰 수 있음.

app = Flask("SuperScrapper")
db = {}

@app.route("/")
def home():
  return render_template("home.html")
  
@app.route("/report")
def report():
  word = request.args.get('word')
  if word :
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template(
    "report.html",
    searchingBy = word,
    resultsNumber =len(jobs),
    jobs = jobs
  )

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")
app.run(host="0.0.0.0")