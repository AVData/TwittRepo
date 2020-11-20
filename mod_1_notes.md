# ML deployment

1. What is deployment?
'use' it for something - use a model

1. ETL -
2. Preprocessing -
3. EDA -
---------------
4. Features -   PCA or LDA
5. Pick Algos -
6. Baseline -
7. Pick a model from baseline -
8. Test and tune as needed -
----------------
9. Deployment -



# (Things to take into account whenever deployment is on the table; consideration is "are these going to be put into productions")
1. Entanglement - If we make a change in the model, what happens to our deployability of it; changing anything changes everything
2. Data Dependency - everything that is done to one, has to be done to the other
3. Configuration (platform) - where is this going to live, am i doing it in java, python, R, etc.
4. Data and Feature Prep - (see above list)
5. Detecting Model Errors -
6. Separation of expertise - working in teams



# Deployment Design Considerations:

1. Building a model to make real time / batch pred.?
2. How often will you need to update the model?
3. Traffic Demand - engineering
4. Size of Data
5. Type of algos/models
6. Can this be done without ML?



# 4 patters to deployment:

1. REST API - Flask (for example) - will work best for batch processing; on the fly predictions (simply building a piece of middle-ware to send data to, opens model, model makes pred, sends data back.)

2. Shared DB (older) -  batch, super high latency

3. Streaming - streaming data, message queue (ingestion pipeline), preds are streamed; sucker is high maintenance, and super costly

4. Mobile (app) - streaming, preds made on the fly, processed on a device

5. PMML (older) - pred modeling markup language



Web App. Dev:

What is Flask?
- Micro Frameworks - Collection of applications that are already written useable to solve problems in applications; we use Flask because of it's size, super small, and can do some heavy lifting.

Why?
- Not a backend service
- Nothing new in Flask, just does what it does.
- Well documented, widespread use
















#
