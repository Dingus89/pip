Touch __init__.py core/__init__.py memory/__init__.py learning/_init__.py
Python3 -m venv lillm 
Source lillm/bin/activate
pip install torch==1.12.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install numpy scikit-learn regex tqdm sqlite-utils flake8
Pip check
sudo nano /etc/systemd/system/pip_llm.service

[Unit]
Description=Pip Local LLM Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/krispyai/pip_llm/run_pip.py
WorkingDirectory=/home/krispyai/pip_llm
Restart=always
User=krispyai

[Install]
WantedBy=multi-user.target

#Type:
Cntrl + o
Enter
Ctrl + x

#Enable with:
sudo systemctl daemon-reload
sudo systemctl enable pip_llm
sudo systemctl start pip_llm
