from dataclasses import dataclass

from src.byt_project.models.scanner_operator import ScannerOperator
from src.byt_project.models.security_officer import SecurityOfficer

# OVERLAPPING OF SEC OFFICER AND SCANNER OP
@dataclass
class ScannerSecurityOfficer(SecurityOfficer, ScannerOperator):
    pass