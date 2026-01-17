from analyst_agent import AnalystAgent

if __name__ == "__main__":
    agent = AnalystAgent()
    topic = "Q3 sales results for Product X"
    result = agent.run(topic)

    print("Topic:", result.topic)
    print("Data points:")
    for dp in result.data_points:
        print("-", dp.text)
