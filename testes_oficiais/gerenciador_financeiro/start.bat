@echo off
echo 🚀 Iniciando Backend e Frontend...

start cmd /k "cd backend-node && npm start"
timeout /t 5
start cmd /k "cd frontend-react && npm start"

echo ✅ Ambos servidores estão iniciando...
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:5000