from dotenv import load_dotenv


load_dotenv()

from graph.graph import app



if __name__ == "__main__":
    print("Test Case Simplifier App")

    print(app.invoke({"question": "your question here",
                      "user_code": "user code here",
                      "language": "python",
                      "baseline_code": "baseline correct code here"}))