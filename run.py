import uvicorn

def main():
    uvicorn.run('main:app', port=8080, reload=True)

if __name__== '__main__':
    main()