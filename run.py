import uvicorn

def main():
    uvicorn.run('main:app', port=9811, reload=True)

if __name__== '__main__':
    main()