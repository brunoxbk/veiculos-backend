class CalculadoraEleitoral:
    def __init__(self, total_eleitores, validos, votos_brancos, nulos):
        """
        Inicializa a calculadora com os dados eleitorais
        
        Args:
            total_eleitores (int): Total de eleitores
            validos (int): Número de votos válidos
            votos_brancos (int): Número de votos em branco
            nulos (int): Número de votos nulos
        """
        self.total_eleitores = total_eleitores
        self.validos = validos
        self.votos_brancos = votos_brancos
        self.nulos = nulos
    
    def percentual_validos(self):
        """
        Calcula o percentual de votos válidos em relação ao total de eleitores
        
        Returns:
            float: Percentual de votos válidos
        """
        return (self.validos / self.total_eleitores) * 100
    
    def percentual_brancos(self):
        """
        Calcula o percentual de votos em branco em relação ao total de eleitores
        
        Returns:
            float: Percentual de votos em branco
        """
        return (self.votos_brancos / self.total_eleitores) * 100
    
    def percentual_nulos(self):
        """
        Calcula o percentual de votos nulos em relação ao total de eleitores
        
        Returns:
            float: Percentual de votos nulos
        """
        return (self.nulos / self.total_eleitores) * 100
    


if __name__ == "__main__":
    calculadora = CalculadoraEleitoral(
        total_eleitores=1000,
        validos=800,
        votos_brancos=150,
        nulos=50
    )
    
    
    print("\nAnálise de votos:")
    print(f"Válidos: {calculadora.percentual_validos():.2f}%")
    print(f"Brancos: {calculadora.percentual_brancos():.2f}%")
    print(f"Nulos: {calculadora.percentual_nulos():.2f}%")
    