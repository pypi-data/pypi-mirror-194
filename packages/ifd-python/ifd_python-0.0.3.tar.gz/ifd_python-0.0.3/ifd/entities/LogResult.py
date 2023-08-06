class LogResult:
    """Contient le log d'une analyse
    step : étape dans le workflow
    startTime : date de début de l'analyse
    stopTime : date de fin de l'analyse
    duration : durée de l'analyse
    result : le résultat de l'analyse; en cas d'erreur, contient le type d'erreur
    message : contient le message d'erreur en cas d'erreur
    """
    def __init__(self, step, startTime, stopTime, duration, result, message):
        self.step = step
        self.startTime = startTime
        self.stopTime = stopTime
        self.duration = duration
        self.result = result
        self.message = message