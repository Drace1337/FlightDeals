import React, { useState, useEffect } from 'react'
import api from '../../services/api'
import './ProfilePage.scss'

const ProfilePage = () => {
	const [profile, setProfile] = useState(null)
	const [editMode, setEditMode] = useState(false)
	const [formData, setFormData] = useState({ name: '', email: '' })

	const [passwordData, setPasswordData] = useState({
		current_password: '',
		new_password: '',
	})
	const [passwordMessage, setPasswordMessage] = useState('')
	const [showPasswordForm, setShowPasswordForm] = useState(false)

	useEffect(() => {
		api
			.get('/profile')
			.then(res => {
				setProfile(res.data)
				setFormData({ name: res.data.name, email: res.data.email })
			})
			.catch(err => console.error(err))
	}, [])

	const handleUpdate = () => {
		api
			.put('/profile', formData)
			.then(() => {
				setProfile({ ...profile, ...formData })
				setEditMode(false)
			})
			.catch(err => console.error(err))
	}

	const handleChangePassword = () => {
		setPasswordMessage('')
		api
			.put('/profile/password', passwordData)
			.then(res => {
				setPasswordMessage(res.data.message)
				setPasswordData({ current_password: '', new_password: '' })
				setShowPasswordForm(false)
			})
			.catch(err => {
				setPasswordMessage(err.response?.data?.message || 'Failed to update password')
			})
	}

	if (!profile) return <div>Loading...</div>

	return (
		<div className='profile-page'>
			<h1>Your Profile</h1>

			{!editMode ? (
				<div className='profile-page__info'>
					<p>
						<strong>Name:</strong> {profile.name}
					</p>
					<p>
						<strong>Email:</strong> {profile.email}
					</p>
					<button onClick={() => setEditMode(true)}>Edit Profile</button>
				</div>
			) : (
				<div className='profile-page__form'>
					<div className='form-group'>
						<label>Name:</label>
						<input
							type='text'
							value={formData.name}
							onChange={e => setFormData({ ...formData, name: e.target.value })}
						/>
					</div>
					<div className='form-group'>
						<label>Email:</label>
						<input
							type='email'
							value={formData.email}
							onChange={e => setFormData({ ...formData, email: e.target.value })}
						/>
					</div>
					<div className='profile-page__actions'>
						<button onClick={handleUpdate}>Save</button>
						<button onClick={() => setEditMode(false)}>Cancel</button>
					</div>
				</div>
			)}

			<hr style={{ margin: '2rem 0' }} />

			<button className='profile-page__toggle-password-btn' onClick={() => setShowPasswordForm(prev => !prev)}>
				{showPasswordForm ? 'Cancel Password Change' : 'Change Password'}
			</button>

			{showPasswordForm && (
				<div className='profile-page__password-form'>
					<h3>Change Password</h3>
					{passwordMessage && <p className='message'>{passwordMessage}</p>}
					<div className='form-group'>
						<label>Current Password:</label>
						<input
							type='password'
							value={passwordData.current_password}
							onChange={e => setPasswordData({ ...passwordData, current_password: e.target.value })}
						/>
					</div>
					<div className='form-group'>
						<label>New Password:</label>
						<input
							type='password'
							value={passwordData.new_password}
							onChange={e => setPasswordData({ ...passwordData, new_password: e.target.value })}
						/>
					</div>
					<button className='profile-page__update-password-btn' onClick={handleChangePassword}>
						Update Password
					</button>
				</div>
			)}
		</div>
	)
}

export default ProfilePage
