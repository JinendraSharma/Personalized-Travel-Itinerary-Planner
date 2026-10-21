import React, { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { tripsAPI } from '../services/api'
import { motion, AnimatePresence } from 'framer-motion'
import {
  ArrowLeft,
  ArrowRight,
  Loader,
  MapPin,
  Calendar,
  Users,
  Sparkles,
  CheckCircle2,
  Globe,
  Waves,
  Mountain,
  UtensilsCrossed,
  Palmtree,
  Camera,
  Music
} from 'lucide-react'

export const CreateTrip = ({ onTripGenerated }) => {
  const navigate = useNavigate()
  const location = useLocation()
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [formData, setFormData] = useState({
    destination: '',
    start_date: '',
    end_date: '',
    travel_style: 'cultural',
    num_travelers: 1,
    budget_per_day: 5000,
    currency: 'INR',
    pace: 'moderate',
    dietary_needs: '',
    interests: ['Culture & History', 'Local Cuisine'],
  })

  const travelStyles = [
    { id: 'cultural', label: 'Cultural & Heritage', icon: Globe, desc: 'Museums, monuments, history & traditions' },
    { id: 'beach', label: 'Beach & Coastal', icon: Waves, desc: 'Sun, sand, water sports & relaxation' },
    { id: 'adventure', label: 'Mountain & Adventure', icon: Mountain, desc: 'Hiking, trekking, nature & thrills' },
    { id: 'foodie', label: 'Foodie & Culinary', icon: UtensilsCrossed, desc: 'Local delicacies, street food & cafes' },
    { id: 'tropical', label: 'Tropical & Nature', icon: Palmtree, desc: 'Forests, wildlife & scenic retreats' },
    { id: 'sightseeing', label: 'Photography & Sights', icon: Camera, desc: 'Iconic viewpoints & photogenic spots' },
    { id: 'nightlife', label: 'Nightlife & Events', icon: Music, desc: 'Live music, clubs & evening vibes' },
  ]

  const interestOptions = [
    'Culture & History',
    'Local Cuisine',
    'Museums & Art',
    'Nature & Parks',
    'Shopping & Bazaars',
    'Nightlife & Lounges',
    'Photography',
    'Architecture',
    'Adventure & Sports',
    'Wellness & Spa',
  ]

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
    if (error) setError('')
  }

  const toggleInterest = (interest) => {
    setFormData((prev) => {
      const exists = prev.interests.includes(interest)
      return {
        ...prev,
        interests: exists
          ? prev.interests.filter((i) => i !== interest)
          : [...prev.interests, interest],
      }
    })
  }

  const validateStep = () => {
    if (step === 1) {
      if (!formData.destination.trim()) {
        setError('Please enter a destination.')
        return false
      }
      if (!formData.start_date || !formData.end_date) {
        setError('Please select both start and end dates.')
        return false
      }
      if (new Date(formData.end_date) < new Date(formData.start_date)) {
        setError('End date cannot be earlier than start date.')
        return false
      }
    }
    return true
  }

  const handleNext = () => {
    if (validateStep()) {
      setError('')
      setStep((prev) => Math.min(prev + 1, 4))
    }
  }

  const handleBack = () => {
    setError('')
    setStep((prev) => Math.max(prev - 1, 1))
  }

  const handleSubmit = async (e) => {
    if (e) e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const generatedTrip = await tripsAPI.planTrip(formData)
      if (onTripGenerated) {
        onTripGenerated(generatedTrip)
      } else {
        navigate('/itinerary', { state: { trip: generatedTrip } })
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate itinerary. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="trip-builder-container">
      {/* Header and Step Progress */}
      <div className="builder-header">
        <div className="steps-indicator">
          {['Destination', 'Style & Pace', 'Preferences', 'Review'].map((label, index) => {
            const stepNum = index + 1
            const isActive = step === stepNum
            const isCompleted = step > stepNum

            return (
              <div key={label} className={`step-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}>
                <div className="step-circle">
                  {isCompleted ? <CheckCircle2 size={18} /> : stepNum}
                </div>
                <span className="step-label">{label}</span>
              </div>
            )
          })}
        </div>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="builder-card">
        <AnimatePresence mode="wait">
          {/* STEP 1: Destination & Dates */}
          {step === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.25 }}
              className="step-content"
            >
              <h2>Where & When are you traveling?</h2>
              <p className="subtitle">Let us know your destination and travel dates.</p>

              <div className="form-group">
                <label>Destination</label>
                <div className="input-with-icon">
                  <MapPin className="input-icon" size={20} />
                  <input
                    type="text"
                    placeholder="e.g. Kyoto, Japan or Goa, India"
                    value={formData.destination}
                    onChange={(e) => handleInputChange('destination', e.target.value)}
                  />
                </div>
              </div>

              <div className="grid-two">
                <div className="form-group">
                  <label>Start Date</label>
                  <div className="input-with-icon">
                    <Calendar className="input-icon" size={20} />
                    <input
                      type="date"
                      value={formData.start_date}
                      onChange={(e) => handleInputChange('start_date', e.target.value)}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>End Date</label>
                  <div className="input-with-icon">
                    <Calendar className="input-icon" size={20} />
                    <input
                      type="date"
                      value={formData.end_date}
                      onChange={(e) => handleInputChange('end_date', e.target.value)}
                    />
                  </div>
                </div>
              </div>

              <div className="form-group">
                <label>Number of Travelers</label>
                <div className="input-with-icon">
                  <Users className="input-icon" size={20} />
                  <input
                    type="number"
                    min="1"
                    max="30"
                    value={formData.num_travelers}
                    onChange={(e) => handleInputChange('num_travelers', parseInt(e.target.value) || 1)}
                  />
                </div>
              </div>
            </motion.div>
          )}

          {/* STEP 2: Travel Style & Pace */}
          {step === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.25 }}
              className="step-content"
            >
              <h2>What is your Travel Style?</h2>
              <p className="subtitle">Choose the vibe that best matches your dream trip.</p>

              <div className="styles-grid">
                {travelStyles.map((style) => {
                  const Icon = style.icon
                  const isSelected = formData.travel_style === style.id
                  return (
                    <div
                      key={style.id}
                      className={`style-card ${isSelected ? 'selected' : ''}`}
                      onClick={() => handleInputChange('travel_style', style.id)}
                    >
                      <Icon size={26} className="style-icon" />
                      <h4>{style.label}</h4>
                      <p>{style.desc}</p>
                    </div>
                  )
                })}
              </div>

              <div className="form-group" style={{ marginTop: '20px' }}>
                <label>Travel Pace</label>
                <div className="pace-options">
                  {[
                    { id: 'relaxed', label: 'Relaxed', desc: 'Fewer stops, plenty of downtime' },
                    { id: 'moderate', label: 'Moderate', desc: 'Balanced sights and breaks' },
                    { id: 'fast-paced', label: 'Fast-Paced', desc: 'See as much as possible' },
                  ].map((p) => (
                    <label
                      key={p.id}
                      className={`pace-card ${formData.pace === p.id ? 'selected' : ''}`}
                    >
                      <input
                        type="radio"
                        name="pace"
                        value={p.id}
                        checked={formData.pace === p.id}
                        onChange={(e) => handleInputChange('pace', e.target.value)}
                      />
                      <strong>{p.label}</strong>
                      <span>{p.desc}</span>
                    </label>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {/* STEP 3: Budget & Preferences */}
          {step === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.25 }}
              className="step-content"
            >
              <h2>Budget & Personal Interests</h2>
              <p className="subtitle">Help our AI personalize activities to your taste and wallet.</p>

              <div className="form-group">
                <label>Daily Budget per Person ({formData.currency})</label>
                <div className="budget-input-wrapper">
                  <input
                    type="number"
                    min="500"
                    step="500"
                    value={formData.budget_per_day}
                    onChange={(e) => handleInputChange('budget_per_day', parseFloat(e.target.value) || 0)}
                  />
                  <select
                    value={formData.currency}
                    onChange={(e) => handleInputChange('currency', e.target.value)}
                  >
                    <option value="INR">INR (₹)</option>
                    <option value="USD">USD ($)</option>
                    <option value="EUR">EUR (€)</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Select Your Interests</label>
                <div className="tags-container">
                  {interestOptions.map((item) => {
                    const isSelected = formData.interests.includes(item)
                    return (
                      <button
                        type="button"
                        key={item}
                        className={`tag-btn ${isSelected ? 'selected' : ''}`}
                        onClick={() => toggleInterest(item)}
                      >
                        {item}
                      </button>
                    )
                  })}
                </div>
              </div>

              <div className="form-group">
                <label>Dietary Needs / Special Notes (Optional)</label>
                <input
                  type="text"
                  placeholder="e.g. Vegetarian, Halal, Jain food, Wheelchair accessible"
                  value={formData.dietary_needs}
                  onChange={(e) => handleInputChange('dietary_needs', e.target.value)}
                />
              </div>
            </motion.div>
          )}

          {/* STEP 4: Review & Generate */}
          {step === 4 && (
            <motion.div
              key="step4"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.25 }}
              className="step-content"
            >
              <h2>Review Your Trip Parameters</h2>
              <p className="subtitle">Everything look good? Click below to generate your custom itinerary!</p>

              <div className="review-summary">
                <div className="summary-row">
                  <span>Destination:</span>
                  <strong>{formData.destination}</strong>
                </div>
                <div className="summary-row">
                  <span>Dates:</span>
                  <strong>{formData.start_date} to {formData.end_date}</strong>
                </div>
                <div className="summary-row">
                  <span>Travelers:</span>
                  <strong>{formData.num_travelers} person(s)</strong>
                </div>
                <div className="summary-row">
                  <span>Travel Style:</span>
                  <strong style={{ textTransform: 'capitalize' }}>{formData.travel_style}</strong>
                </div>
                <div className="summary-row">
                  <span>Daily Budget:</span>
                  <strong>{formData.budget_per_day} {formData.currency}</strong>
                </div>
                <div className="summary-row">
                  <span>Pace:</span>
                  <strong style={{ textTransform: 'capitalize' }}>{formData.pace}</strong>
                </div>
                <div className="summary-row">
                  <span>Interests:</span>
                  <strong>{formData.interests.join(', ') || 'General sightseeing'}</strong>
                </div>
                {formData.dietary_needs && (
                  <div className="summary-row">
                    <span>Dietary / Notes:</span>
                    <strong>{formData.dietary_needs}</strong>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Navigation Buttons */}
        <div className="builder-actions">
          {step > 1 && (
            <button type="button" className="btn-secondary" onClick={handleBack} disabled={loading}>
              <ArrowLeft size={16} /> Back
            </button>
          )}

          <div style={{ marginLeft: 'auto' }}>
            {step < 4 ? (
              <button type="button" className="btn-primary" onClick={handleNext}>
                Continue <ArrowRight size={16} />
              </button>
            ) : (
              <button type="button" className="btn-generate" onClick={handleSubmit} disabled={loading}>
                {loading ? (
                  <>
                    <Loader className="spin" size={18} /> Generating Custom Plan...
                  </>
                ) : (
                  <>
                    <Sparkles size={18} /> Generate Itinerary
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default CreateTrip
