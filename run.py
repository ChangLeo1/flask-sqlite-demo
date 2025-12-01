from app import create_app

app = create_app()

if __name__ == '__main__':
    # host 可改为 '0.0.0.0' 以便局域网访问
    app.run(debug=True)


