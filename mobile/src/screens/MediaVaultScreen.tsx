import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView, Alert } from 'react-native';

export default function MediaVaultScreen({ navigation }: any) {
  const [photoUri, setPhotoUri] = useState<string | null>(null);
  const [audioDuration, setAudioDuration] = useState<number | null>(null);

  const handleSelectPhoto = () => {
    // In production: ImagePicker.launchImageLibraryAsync
    setPhotoUri("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=300");
    Alert.alert("Photo Selected", "Front-facing portrait identified. Face clarity: 96%");
  };

  const handleUploadAudio = () => {
    // In production: DocumentPicker or audio recorder
    setAudioDuration(24);
    Alert.alert("Voice Sample Uploaded", "Audio length: 24s. Noise suppression active. Voice similarity score: High.");
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Loved One's Memory Vault</Text>
      <Text style={styles.subtitle}>
        Upload clear photos and WhatsApp voice notes to build their living story companion.
      </Text>

      {/* Photo Section */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>1. Reference Portrait</Text>
        <Text style={styles.cardDesc}>A clear, front-facing photo where eyes and mouth are visible.</Text>
        
        {photoUri ? (
          <Image source={{ uri: photoUri }} style={styles.previewImage} />
        ) : (
          <TouchableOpacity style={styles.uploadButton} onPress={handleSelectPhoto}>
            <Text style={styles.uploadButtonText}>Select Photo</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Audio Section */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>2. Voice Notes / Samples</Text>
        <Text style={styles.cardDesc}>Upload voice notes (.m4a, .ogg, .wav). 15 to 60 seconds is ideal.</Text>

        <TouchableOpacity style={styles.uploadButton} onPress={handleUploadAudio}>
          <Text style={styles.uploadButtonText}>
            {audioDuration ? `✓ Uploaded (${audioDuration}s clean voice)` : "Import Audio Note"}
          </Text>
        </TouchableOpacity>
      </View>

      {/* Action Button */}
      <TouchableOpacity 
        style={[styles.primaryButton, (!photoUri || !audioDuration) && styles.disabledButton]}
        disabled={!photoUri || !audioDuration}
        onPress={() => navigation.navigate('StoryStudio')}
      >
        <Text style={styles.primaryButtonText}>Continue to Story Studio →</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A', padding: 20 },
  title: { fontSize: 24, fontWeight: '700', color: '#F8FAFC', marginBottom: 8, marginTop: 40 },
  subtitle: { fontSize: 14, color: '#94A3B8', marginBottom: 24, lineHeight: 20 },
  card: { backgroundColor: '#1E293B', padding: 18, borderRadius: 16, marginBottom: 16 },
  cardTitle: { fontSize: 16, fontWeight: '600', color: '#F1F5F9', marginBottom: 4 },
  cardDesc: { fontSize: 13, color: '#64748B', marginBottom: 12 },
  uploadButton: { borderWidth: 1, borderColor: '#38BDF8', borderStyle: 'dashed', borderRadius: 10, padding: 14, alignItems: 'center' },
  uploadButtonText: { color: '#38BDF8', fontWeight: '600' },
  previewImage: { width: 100, height: 100, borderRadius: 50, alignSelf: 'center', marginTop: 8 },
  primaryButton: { backgroundColor: '#38BDF8', borderRadius: 12, padding: 16, alignItems: 'center', marginTop: 16, marginBottom: 40 },
  disabledButton: { backgroundColor: '#334155' },
  primaryButtonText: { color: '#0F172A', fontWeight: '700', fontSize: 16 }
});
