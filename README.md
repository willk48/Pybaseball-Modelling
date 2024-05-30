# Pybaseball-Modelling

This is the final project for an Applied Machine Learning class that I completed in the spring of 2024 with students Max Wassarman and Jack Page. \\The program uses a LASSO regression to predict next_season WAR values for qualified players. This data is used to return breakout player candidates for future seasons. Candidates can be filtered with command line arguments in the following form:\  python baseball.py [WAR_Increase] [Max_Age] [Max_War]

**WAR_Increase**:The selected value is the increase from real recorded WAR and future projected WAR. The default value is 1.25\
**Max_Age**:The selected value is the maximum age for players to be considered for a breakout. default=27\
**Max_War**:The maximum previous season WAR to be considered. Players with higher WARs are not typically considered breakout players. default=3\
