name: Build APK

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install Dependencies
      run: |
        pip install -r requirements.txt
        pip install cookiecutter

    - name: Setup Java
      uses: actions/setup-java@v3
      with:
        distribution: 'temurin'
        java-version: '17'

    - name: Setup Android SDK
      uses: android-actions/setup-android@v3

    - name: Build APK (Auto-Confirm)
      run: |
        # 这里的 "yes" 就是自动点头机器
        # 它会疯狂输入 y，防止程序卡在问答环节
        yes | flet build apk --verbose

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: finance-app-release
        path: build/apk/app-release.apk


