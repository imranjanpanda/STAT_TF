# STAT_TF

 You can install Terraform by following these steps:

1. **Download the Terraform binary**:
   ```sh
   wget https://releases.hashicorp.com/terraform/1.0.11/terraform_1.0.11_linux_amd64.zip
   ```

2. **Unzip the downloaded file**:
   ```sh
   unzip terraform_1.0.11_linux_amd64.zip
   ```

3. **Move the Terraform binary to a directory included in your system's `PATH`**:
   ```sh
   sudo mv terraform /usr/local/bin/
   ```

4. **Verify the installation**:
   ```sh
   terraform -v
   ```
5. **initialize terraform**:
   ```sh
   terraform init
   ```
6. **Run terraform plan**:
   ```sh
   terraform plan
   ```
7. **Run terraform apply**:
   ```sh
   terraform apply
   ```
8. **optional-- Run terraform destroy**:
   ```sh
   terraform destroy
   ```