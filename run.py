from app import create_app

app = create_app()  #run whole projectt execution start

if __name__ == "__main__":
    app.run(debug=True)