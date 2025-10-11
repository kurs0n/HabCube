echo "Konfiguracja środowiska HabCube"

# Dodaj export CURRENT_UID do .bashrc jeśli jeszcze nie istnieje
if ! grep -q "CURRENT_UID" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# HabCube - auto export CURRENT_UID for Docker" >> ~/.bashrc
    echo 'export CURRENT_UID=$(id -u):$(id -g)' >> ~/.bashrc
    echo "Dodano export CURRENT_UID do ~/.bashrc"
else
    echo "CURRENT_UID już istnieje w ~/.bashrc"
fi

# Export dla bieżącej sesji
export CURRENT_UID=$(id -u):$(id -g)
echo "Wyeksportowano CURRENT_UID dla bieżącej sesji: $CURRENT_UID"

echo ""
echo "Teraz można użyć:"
echo "  docker-compose up -d --build --force-recreate"
echo "  lub: make init"
echo ""
echo "Otwórz nowy terminal lub uruchom: source ~/.bashrc"
