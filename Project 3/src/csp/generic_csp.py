class CSP:
    def __init__(self, variables, domains, neighbors, constraint):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraint = constraint