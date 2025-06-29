import json
import os
from typing import Dict, Any, Optional

class UserDataLoader:
    def __init__(self, data_directory: str = "user_data"):
        self.data_directory = data_directory
        self.domains = ["methylation", "metagenomics", "whole_exome", "proteomics", "transcriptomics", "whole_genome"]
    
    def load_user_report(self, user_id: str, domain: str = None) -> Optional[Dict[str, Any]]:
        """
        Load user report data from file
        
        Args:
            user_id: User identifier
            domain: Specific domain to load (optional)
        """
        if domain:
            # Load domain-specific report
            file_path = os.path.join(self.data_directory, domain, f"{user_id}_report.txt")
        else:
            # Load general report (backward compatibility)
            file_path = os.path.join(self.data_directory, f"{user_id}_report.txt")
        
        if not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading user data for {user_id} ({domain}): {e}")
            return None
    
    def get_available_users(self) -> list:
        """
        Get list of available user IDs across all domains
        """
        users = set()
        if os.path.exists(self.data_directory):
            # Check general user data directory
            for filename in os.listdir(self.data_directory):
                if filename.endswith("_report.txt"):
                    user_id = filename.replace("_report.txt", "")
                    users.add(user_id)
            
            # Check domain-specific directories
            for domain in self.domains:
                domain_path = os.path.join(self.data_directory, domain)
                if os.path.exists(domain_path):
                    for filename in os.listdir(domain_path):
                        if filename.endswith("_report.txt"):
                            user_id = filename.replace("_report.txt", "")
                            users.add(user_id)
        return sorted(list(users))
    
    def get_available_domains(self, user_id: str) -> list:
        """
        Get list of available domains for a specific user
        """
        available_domains = []
        
        # Check general user data
        general_file = os.path.join(self.data_directory, f"{user_id}_report.txt")
        if os.path.exists(general_file):
            available_domains.append("general")
        
        # Check domain-specific data
        for domain in self.domains:
            domain_file = os.path.join(self.data_directory, domain, f"{user_id}_report.txt")
            if os.path.exists(domain_file):
                available_domains.append(domain)
        
        return available_domains
    
    def user_exists(self, user_id: str, domain: str = None) -> bool:
        """
        Check if user data exists
        
        Args:
            user_id: User identifier
            domain: Specific domain to check (optional)
        """
        if domain:
            file_path = os.path.join(self.data_directory, domain, f"{user_id}_report.txt")
        else:
            file_path = os.path.join(self.data_directory, f"{user_id}_report.txt")
        return os.path.exists(file_path)
    
    def get_all_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Get all available data for a user across all domains
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with domain as key and report data as value
        """
        all_data = {}
        
        # Get general data
        general_data = self.load_user_report(user_id)
        if general_data:
            all_data["general"] = general_data
        
        # Get domain-specific data
        for domain in self.domains:
            domain_data = self.load_user_report(user_id, domain)
            if domain_data:
                all_data[domain] = domain_data
        
        return all_data 