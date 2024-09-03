export async function registerUser(username, password, isAdmin = false) {
    try {
      // Log message to verify code execution
      console.log("Executing registerUser function");
  
      // Send POST request to the /register endpoint
      const response = await fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
          is_admin: isAdmin, // Send is_admin as expected by the backend
        }),
      });
  
      // Check if the response is not OK
      if (!response.ok) {
        // Extract and throw the error message from the response
        const errorData = await response.json();
        throw new Error(errorData.error || 'Registration failed');
      }
  
      // Parse and return the response JSON data
      const data = await response.json();
      return data;
    } catch (error) {
      // Throw any error encountered during the request
      throw error;
    }
  }
  
  export async function loginUser(username, password) {
    try {
      // Log message to verify code execution
      console.log("Executing loginUser function");
  
      // Send POST request to the /login endpoint
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });
  
      // Check if the response is not OK
      if (!response.ok) {
        // Extract and throw the error message from the response
        const errorData = await response.json();
        throw new Error(errorData.error || 'Login failed');
      }
  
      // Parse and return the response JSON data (access token)
      const data = await response.json();
      return data;
    } catch (error) {
      // Throw any error encountered during the request
      throw error;
    }
  }
  