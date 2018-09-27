# Data wrangling on OpenStreetMaps data
In this project -- which is part of the Udacity Data Analysis Nanodegree -- I will apply some data munging techniques, such as assessing the quality of the data for validity, accuracy, completeness, consistency and uniformity, to clean an specific area from OpenStreetMap data. After it, in order to try database manipulation in Python, I will load the cleaned data to a MongoDB collection (installed locally in my machine) and apply some simple statistics on it.

## Choosing an OpenStreetRegion: Missões!
My region of interest in this project is Santo Ângelo, a countryside small city in the southest estate of Brazil which were my birthplace. However, since there's few data for this city and, for this project, I'm supposed to deal with databases larger than 50MB, I will consider all the neighboring cities, which in turn constitute the "Missões" region [1] and represent an important chapter in the South American history, since the first settlements were founded during the Spanish colonial missions [2].  

Although today there are 46 municipalities composing this region, in the early eighteenth century there were only 7 villages, nowadays known in Portuguese as the "Sete Povos das Missões":
- São Miguel das Missões  
- Santo Ângelo  
- São Borja  
- São Nicolau  
- São Luiz Gonzaga  
- São Lourenço  
- Entre-Ijuís (where remains the ruins of the town of São João Batista)  

## Getting data:
The data was obtained from ... 

After downloading the data, the first step I should do if I did not know the data model would be a simple "less" shell command to figure out what kind of data were in it. Since OpenStreetMaps provides us with a data model, we can move forward to the next step: auditing data.  


## Auditing data:  
The auditing questions comes when we start exploring the data or, if it's the case we have a prior knowledge of the problem, we already have in mind some issues to investigate. Considering there are available on Internet some similar analysis on OpenStreetMap data [3,4]; and also considering my previous knowledge about this region, I intend to audit the following issues:  
A. Quantitative aspects:   
- Do the dataset contains more than the 46 current cities of the Missões region?
- Do I have information from the 6 cities evolved form the ancient villages?

B. Qualitative aspects:  
- Are the cities names correct?
- Are the street names correct?
- Are there abbreviations?
- Are the postal codes consistent?  




## References
[1] https://en.wikipedia.org/wiki/Miss%C3%B5es
[2] https://en.wikipedia.org/wiki/Spanish_missions_in_South_America
[3] https://jasonicarter.github.io/openstreetmap-data-wrangling-mongodb/
[4] https://eberlitz.github.io/2015/09/18/data-wrangle-openstreetmaps-data/