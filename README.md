# OrdersApi
An automated test suite for a RESTful API that simulates a trading platform with WebSocket support.
1. install python3.8
2. create env: python3 -m venv env
3. activate env: .\env\Scripts\activate 
4. install dependencies: pip install -r requirements.txt
5. install wsl: wsl --install
6. install docker desktop, run docker
7. run command: docker run --name mongo -p 27017:27017 -d mongodb/mongodb-community-server:latest
8. pytest --html=report.html