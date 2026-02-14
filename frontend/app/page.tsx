// frontend/app/page.tsx
'use client';

import { useState } from 'react';

export default function HomePage() {
  // Form state
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [file, setFile] = useState<File | null>(null);

  // UI state
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);

  // Input style
  const inputStyle = {
    display: 'block',
    width: '100%',
    padding: '15px',
    marginBottom: '20px',
    border: '1px solid #ccc',
    borderRadius: '10px',
    fontSize: '16px'
  };

  const handleUpload = async () => {
    if (!name || !email || !phone || !file) {
      alert('Please fill all fields and select a resume');
      return;
    }

    setUploading(true);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);
    formData.append('email', email);
    formData.append('phone', phone);
    formData.append('job_id', 'senior-software-engineer');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/upload-resume', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error('Upload failed');

      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert('Upload failed. See console for details.');
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px'
    }}>
      <div style={{
        background: 'white',
        padding: '40px',
        borderRadius: '20px',
        maxWidth: '500px',
        width: '100%',
        boxShadow: '0 20px 60px rgba(0,0,0,0.3)'
      }}>
        {/* Title */}
        <h1 style={{ 
          fontSize: '32px', 
          fontWeight: 'bold', 
          textAlign: 'center',
          marginBottom: '10px',
          color: '#333'
        }}>
          🎙️ Voice AI Screening
        </h1>
        
        <p style={{ 
          textAlign: 'center', 
          color: '#666',
          marginBottom: '30px'
        }}>
          Fill your details and upload your resume
        </p>

        {/* Upload Form */}
        {!result && (
          <>
            <input
              type="text"
              placeholder="Full Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              style={inputStyle}
            />

            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={inputStyle}
            />

            <input
              type="tel"
              placeholder="Phone Number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              style={inputStyle}
            />

            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              style={{
                display: 'block',
                width: '100%',
                padding: '15px',
                marginBottom: '20px',
                border: '2px dashed #ccc',
                borderRadius: '10px',
                cursor: 'pointer'
              }}
            />

            <button
              onClick={handleUpload}
              disabled={!file || uploading}
              style={{
                width: '100%',
                padding: '15px',
                fontSize: '18px',
                fontWeight: 'bold',
                color: 'white',
                background: uploading ? '#ccc' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none',
                borderRadius: '10px',
                cursor: uploading ? 'not-allowed' : 'pointer'
              }}
            >
              {uploading ? 'Uploading...' : 'Upload Resume'}
            </button>
          </>
        )}

        {/* Result */}
        {result && (
          <div style={{
            padding: '20px',
            background: '#f0f9ff',
            borderRadius: '10px',
            border: '2px solid #3b82f6'
          }}>
            <h2 style={{ 
              fontSize: '24px', 
              fontWeight: 'bold',
              color: '#1e40af',
              marginBottom: '15px'
            }}>
              ✅ Upload Successful!
            </h2>
            
            <div style={{ fontSize: '16px', lineHeight: '1.8', color: '#333' }}>
              <p><strong>Name:</strong> {result.candidate?.name || name}</p>
              <p><strong>Email:</strong> {result.candidate?.email || email}</p>
              <p><strong>Phone:</strong> {result.candidate?.phone || phone}</p>
            </div>

            <button
              onClick={() => {
                setResult(null);
                setFile(null);
                setName('');
                setEmail('');
                setPhone('');
              }}
              style={{
                marginTop: '20px',
                width: '100%',
                padding: '12px',
                background: '#6b7280',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
            >
              Upload Another
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
