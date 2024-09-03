// Base URL of the Flask API
const API_URL = 'https://your-api-url.com';  // Replace with your actual API URL

// Function to handle JWT token
const getToken = (): string | null => {
  return localStorage.getItem('token');  // Replace with your token storage mechanism
};

// Helper function to handle HTTP requests
const request = async (url: string, method: string, body?: object): Promise<any> => {
  const token = getToken();
  const headers: { [key: string]: string } = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${url}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || 'Network response was not ok');
  }

  return response.json();
};

// User API calls
export const register = (username: string, password: string): Promise<any> => {
  return request('/register', 'POST', { username, password });
};

export const login = (username: string, password: string): Promise<any> => {
  return request('/login', 'POST', { username, password });
};

// Salon API calls
export const createSalon = (name: string, address: string, phone: string): Promise<any> => {
  return request('/salon', 'POST', { name, address, phone });
};

export const getSalon = (id: number): Promise<any> => {
  return request(`/salon/${id}`, 'GET');
};

export const updateSalon = (id: number, name?: string, address?: string, phone?: string): Promise<any> => {
  return request(`/salon/${id}`, 'PUT', { name, address, phone });
};

export const deleteSalon = (id: number): Promise<void> => {
  return request(`/salon/${id}`, 'DELETE');
};

export const getSalons = (page: number = 1, perPage: number = 10): Promise<any> => {
  return request('/salons', 'GET', { params: { page, per_page: perPage } });
};

// Service API calls
export const createService = (name: string, duration: number, price: number, salonId: number): Promise<any> => {
  return request('/service', 'POST', { name, duration, price, salon_id: salonId });
};

// Appointment API calls
export const createAppointment = (dateTime: string, serviceId: number, clientName: string, clientPhone: string): Promise<any> => {
  return request('/appointment', 'POST', { date_time: dateTime, service_id: serviceId, client_name: clientName, client_phone: clientPhone });
};

export const getAvailableSlots = (salonId: number, serviceId: number, date: string): Promise<any> => {
  return request('/available_slots', 'GET', { salon_id: salonId, service_id: serviceId, date });
};
