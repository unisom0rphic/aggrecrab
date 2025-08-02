# **Contributing Guide**  
## **How to Contribute**  

### **1. Reporting Bugs**  
- Check the [Issues](https://github.com/unisom0rphic/aggrecrab/issues) to see if the bug has already been reported.  
- If not, open a **new issue** with a clear title and description.  
- Include steps to reproduce, expected vs. actual behavior, and screenshots (if applicable).  

### **2. Suggesting Enhancements**  
- Open an issue with the **"enhancement"** label.  
- Describe the feature and why it would be useful.  
- If possible, provide mockups or examples.  

### **3. Making Code Contributions**  
#### **Fork & Clone the Repository**  
```bash
git clone https://github.com/unisom0rphic/aggrecrab.git
cd aggrecrab
```  

#### **Set Up the Development Environment**  
- Install dependencies:  
  ```bash
  pip install -r requirements.txt  # Use python3.11
  ```

#### **Create a Branch**  
```bash
git checkout -b feature/your-feature-name  # or fix/your-bug-fix
```  

#### **Make Your Changes**  
- Write tests if applicable.
- Update documentation if needed.  

#### **Commit & Push**  
- Write clear, concise commit messages. Make sure to follow [**Conventional Commits**](https://www.conventionalcommits.org/) convention 
  ```bash
  git commit -m "feat: add new login button"  
  git push origin your-branch-name  
  ```  

#### **Open a Pull Request (PR)**  
- Go to the [Pull Requests](https://github.com/unisom0rphic/aggrecrab/pulls) page.  
- Click **"New Pull Request"** and select your branch.  
- Fill in the PR template (if available).  
- Wait for review and address feedback if needed.  

## **Code Guidelines**  
- Follow [PEP 8](https://pep8.org/)
- Write meaningful comments and docstrings.  
- Keep commits atomic and well-described.  

We appreciate your contributions! 🎉
