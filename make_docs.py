import json, os, re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape
D=json.load(open('scripts/content.json'));os.makedirs('dist/docs',exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
if os.path.exists(font):
 pdfmetrics.registerFont(TTFont('Body',font));pdfmetrics.registerFont(TTFont('Bold',font.replace('Sans.ttf','Sans-Bold.ttf')))
else: pass
styles=getSampleStyleSheet()
for n in ['Normal','BodyText']:styles[n].fontName='Body';styles[n].fontSize=9.3;styles[n].leading=15
styles.add(ParagraphStyle(name='TitleIron',fontName='Bold',fontSize=30,leading=34,textColor=colors.HexColor('#182119'),spaceAfter=18))
styles.add(ParagraphStyle(name='SectionIron',fontName='Bold',fontSize=15,leading=20,textColor=colors.HexColor('#293b2b'),spaceBefore=12,spaceAfter=7,keepWithNext=True))
styles.add(ParagraphStyle(name='SmallIron',fontName='Body',fontSize=8,leading=12,textColor=colors.HexColor('#596252')))
styles.add(ParagraphStyle(name='Kicker',fontName='Bold',fontSize=9,leading=14,textColor=colors.HexColor('#877038'),spaceAfter=15))
def P(t,s='BodyText'):return Paragraph(escape(str(t)).replace('\n','<br/>'),styles[s])
def table(rows,widths=None):
 t=Table([[P(v,'SmallIron') for v in row]for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7e4d6')),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#9f9e85')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d8dcd0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));return t
class Cycle(Flowable):
 def __init__(self,labels):Flowable.__init__(self);self.labels=labels;self.width=480;self.height=85
 def draw(self):
  c=self.canv
  for i,t in enumerate(self.labels):
   x=i*160;c.setFillColor(colors.HexColor('#e7e9de'));c.roundRect(x,15,145,55,4,fill=1,stroke=0);c.setFillColor(colors.HexColor('#34432f'));c.setFont('Bold',8);c.drawString(x+12,49,f'0{i+1}');c.setFont('Body',9);c.drawString(x+12,30,t)
   if i<2:c.setStrokeColor(colors.HexColor('#a99b68'));c.line(x+147,42,x+157,42)
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#a6ad99'));c.line(54,48,541,48);c.setFont('Body',7);c.setFillColor(colors.HexColor('#5a6552'));c.drawString(54,34,'THE IRON JOURNAL  /  FROM ZERO TO BUILT');c.drawRightString(541,34,f'{doc.page}');c.drawString(54,809,'EDUCATION / PRACTICE / REFLECTION')
for i,ch in enumerate(D['chapters']):
 story=[P(f'CHAPTER {i:02d}  /  {ch["tag"]}','Kicker'),P(ch['title'],'TitleIron'),P(ch['line'],'SectionIron'),P(ch['desc']),Spacer(1,15),P('How to use this guide','SectionIron'),P('Read the explanations, try the practical examples and complete the worksheet. All training logs and menus are illustrative. Use the website for interactive tools; this document remains useful offline.'),Cycle(['Understand','Put into practice','Review']),P('Scope and safety','SectionIron'),P('General education for adults, not a medical diagnosis, personalized treatment or a guaranteed transformation. Stop exercise for sharp pain or unusual symptoms. A qualified clinician, dietitian or coach can help when individual circumstances require assessment.'),P('What you will learn','SectionIron')]
 for j,l in enumerate(ch['lessons']):story.append(P(f'{j+1:02d}. {l[0]}'))
 story.append(PageBreak())
 for j,l in enumerate(ch['lessons']):
  story.append(KeepTogether([P(f'{j+1:02d} / {l[0]}','SectionIron'),P(l[1]),Spacer(1,6),P('PUT IT INTO PRACTICE: '+l[2],'SmallIron'),Spacer(1,6)]))
 story.append(PageBreak());story.append(P('Practical reference','TitleIron'))
 if i==1:
  story.append(table([['Muscle group','Location & action','Exercise examples']]+[[m[0],m[2]+'. '+m[3],m[4]]for m in D['muscles']],[95,250,142]))
 elif i==3:
  story.append(P('Exercise technique handbook','SectionIron'))
  for e in D['exercises']:
   story.extend([P(e[0],'SectionIron'),P('Primary: '+e[1]+' | Secondary: '+e[2]+' | Equipment: '+e[3]),table([['Setup',e[4]],['Execution',e[5]],['Breathing',e[6]],['Common mistakes',e[7]],['Safety',e[8]],['Alternative',e[9]]],[100,387]),Spacer(1,8)])
 elif i in [6,7]:
  story.extend([P('Food composition estimates','SectionIron'),P('Approximate values per 100 g of edible food in the stated condition. Generic estimates vary by brand, recipe and preparation. Price assumptions in the website are editable examples, not live market prices.'),table([['Food / condition','kcal','Protein g','Carbs g','Fat g']]+[[f[0]+' / '+f[1],f[2],f[3],f[4],f[5]]for f in D['foods']],[235,60,64,64,64]),P('Calculation example','SectionIron'),P('For a hypothetical 25-year-old male weighing 70 kg at 175 cm: resting expenditure = 10 × 70 + 6.25 × 175 − 5 × 25 + 5 = 1,673.75 kcal/day. At an assumed activity multiplier of 1.55, TDEE is approximately 2,594 kcal/day. This is an estimate, not a measurement.'),P('The website uses example goal adjustments of +8% for gradual gain or −10% for gradual loss. Protein is allocated at 1.6 g/kg, fat at 30% of target energy, and carbohydrate receives the remainder. These defaults are teaching assumptions, not individual prescriptions.'),P('A practical student meal','SectionIron'),P('An example plate can combine cooked rice, plain cooked dal, curd and vegetables. Add a protein side that fits preferences and needs. Record the amount and whether it is raw or cooked. Include added oil. A single plate does not establish a complete day of nutrition.')])
 elif i==8:
  for s in D['supplements']:story.extend([P(s[0],'SectionIron'),table([['Evidence context',s[1]],['Potential role',s[2]],['Limitations',s[3]],['Safety / individual advice',s[4]]],[110,377])])
 elif i in [4,5,12]:
  story.extend([P('Example training week','SectionIron'),P('An editable beginner example; start with manageable loads and comfortable range. This is not a personalized prescription.'),table([['Day','Movements','Example work'],['Monday','Goblet squat, push-up, cable row','2 sets each; controlled reps'],['Wednesday','Romanian deadlift, pulldown, shoulder press','2 sets each; controlled reps'],['Friday','Split squat, dumbbell press, row','2 sets each; controlled reps'],['Other days','Rest or comfortable light activity','Adjust to recovery']],[85,260,142]),P('Example double progression','SectionIron'),table([['Session','Load','Repetitions','Decision'],['A','10 kg','10 / 10 / 9','Practice at same load'],['B','10 kg','11 / 10 / 10','Keep technique consistent'],['C','10 kg','12 / 12 / 12','Consider smallest load increase'],['D','Next suitable load','Return toward 8 reps','Review effort and control']],[70,100,120,197]),P('These sessions are fictional and have no promised dates. Progression should follow readiness rather than an obligation to lift more every workout.')])
 elif i==9:
  story.extend([Cycle(['Train','Nourish','Recover']),P('Recovery planning table','SectionIron'),table([['Observation','A useful response'],['One difficult workout','Review context before changing the plan'],['Late caffeine and poor sleep','Try an earlier cut-off and a consistent schedule'],['Repeated performance decline','Review total workload and recovery'],['Persistent fatigue or sleep problems','Seek qualified assessment']],[220,267])])
 elif i==10:
  story.extend([P('Physique tracking workbook','SectionIron'),table([['Date','Weight kg','Waist cm','Sleep h','Context']]+[['____________','________','________','_______','________________']for _ in range(10)],[90,80,80,70,167]),Spacer(1,20),table([['Date','Exercise','Load kg','Sets × reps','RIR']]+[['________','_________________','_______','___________','____']for _ in range(8)],[80,160,80,100,67])])
 elif i==11:
  story.append(table([['Observation','Check first','Possible next step'],['Plateau','Comparable logs, attendance, effort','Make one small adjustment'],['Scale fluctuation','Water, food, cycle and measurement conditions','Review a longer trend'],['Poor recovery','Sleep, food, life stress and workload','Reduce unnecessary demand'],['Persistent or sharp pain','Stop the provoking activity','Seek qualified assessment']],[120,185,182]))
 else:
  story.extend([Cycle(['Signal','Recovery','Adaptation']),table([['Principle','Practical meaning'],['Consistency','Choose a routine you can repeat'],['Appropriate demand','Use controlled effort without chasing soreness'],['Recovery','Make room for food, rest and sleep'],['Review','Record useful observations and adapt']],[145,342])])
 story.extend([PageBreak(),P('Your study worksheet','TitleIron'),P('Knowledge check','SectionIron'),P(ch['quiz'][0])])
 for k,a in enumerate(ch['quiz'][1]):story.append(P(f'{chr(65+k)}. {a}'))
 story.extend([Spacer(1,12),P('Reflect and apply','SectionIron'),table([['Prompt','Your response'],['One idea I can explain in my own words','\n\n'],['One action I can try this week','\n\n'],['What I will observe or measure','\n\n'],['What would make me seek professional guidance','\n\n'],['My next review date','\n']],[220,267]),P('Chapter summary','SectionIron'),P(ch['summary']),P('Answer and explanation','SectionIron'),P(chr(65+ch['quiz'][2])+'. '+ch['quiz'][3]),PageBreak(),P('Sources & limitations','TitleIron'),P('These sources inform the educational principles. Original examples and planning templates are not study findings. No institution listed below endorses this journal. References checked November 2026.')])
 for idx in ch['refs']:
  s=D['sources'][idx];story.extend([P(s[0]+' — '+s[1],'SectionIron'),Paragraph(f'<link href="{escape(s[2])}" color="#586b40">{escape(s[2])}</link>',styles['SmallIron'])])
 story.extend([Spacer(1,20),P('Interpretation matters','SectionIron'),P('Research describes groups under particular conditions. Individual responses vary. The website models are simplified illustrations, not precise physiological simulations. Food values and calorie estimates are approximate. Use consistent observation and individualized professional support when needed.')])
 doc=SimpleDocTemplate(f'dist/docs/chapter-{i:02d}.pdf',pagesize=(595.28,841.89),rightMargin=54,leftMargin=54,topMargin=60,bottomMargin=64,title=f'The Iron Journal - {ch["title"]}',author='The Iron Journal')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 print(f'Created chapter {i:02d}')
