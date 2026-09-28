import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, Alert } from 'react-native';

const TEMPLATES = [
  { id: 'bedtime_story', label: '🌙 Bedtime Story' },
  { id: 'birthday_wish', label: '🎂 Birthday Wish' },
  { id: 'milestone_congrats', label: '🎓 Milestone' },
  { id: 'life_advice', label: '💡 Words of Love' },
];

export default function StoryStudioScreen({ navigation }: any) {
  const [selectedCategory, setSelectedCategory] = useState('bedtime_story');
  const [title, setTitle] = useState('The Starlight Blanket');
  const [script, setScript] = useState(
    "Goodnight my brave champion. Look up at the stars tonight. Remember how proud I am of you, and that my love is always wrapped around you like a warm blanket. Sweet dreams!"
  );

  const handleGenerate = () => {
    Alert.alert(
      "Rendering Queued",
      "Your tribute video is generating in the cloud. Once ready, it will be placed in the Guardian Review Gate for your inspection.",
      [{ text: "OK", onPress: () => navigation.navigate('GuardianGate') }]
    );
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Story Studio</Text>
      <Text style={styles.subtitle}>
        Write a heartwarming story or message for the kids in their father's voice.
      </Text>

      {/* Category Selection */}
      <Text style={styles.sectionLabel}>Select Milestone Occasion</Text>
      <View style={styles.categoryRow}>
        {TEMPLATES.map((t) => (
          <TouchableOpacity
            key={t.id}
            style={[styles.categoryBadge, selectedCategory === t.id && styles.categoryBadgeActive]}
            onPress={() => setSelectedCategory(t.id)}
          >
            <Text style={[styles.categoryText, selectedCategory === t.id && styles.categoryTextActive]}>
              {t.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Title */}
      <Text style={styles.sectionLabel}>Story Title</Text>
      <TextInput
        style={styles.input}
        value={title}
        onChangeText={setTitle}
        placeholder="Enter title"
        placeholderTextColor="#64748B"
      />

      {/* Script */}
      <Text style={styles.sectionLabel}>Story Script (Spoken by Dad)</Text>
      <TextInput
        style={[styles.input, styles.textArea]}
        value={script}
        onChangeText={setScript}
        multiline
        numberOfLines={5}
        placeholder="Write the words he would say..."
        placeholderTextColor="#64748B"
      />
      <Text style={styles.characterCount}>Est. Duration: ~20 seconds ({script.length} chars)</Text>

      {/* Submit Button */}
      <TouchableOpacity style={styles.primaryButton} onPress={handleGenerate}>
        <Text style={styles.primaryButtonText}>Generate Story Video →</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A', padding: 20 },
  title: { fontSize: 24, fontWeight: '700', color: '#F8FAFC', marginBottom: 8, marginTop: 40 },
  subtitle: { fontSize: 14, color: '#94A3B8', marginBottom: 20, lineHeight: 20 },
  sectionLabel: { fontSize: 14, fontWeight: '600', color: '#CBD5E1', marginBottom: 8, marginTop: 12 },
  categoryRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 16 },
  categoryBadge: { backgroundColor: '#1E293B', paddingVertical: 8, paddingHorizontal: 12, borderRadius: 20, borderWidth: 1, borderColor: '#334155' },
  categoryBadgeActive: { backgroundColor: '#0284C7', borderColor: '#38BDF8' },
  categoryText: { color: '#94A3B8', fontSize: 13, fontWeight: '500' },
  categoryTextActive: { color: '#FFFFFF', fontWeight: '700' },
  input: { backgroundColor: '#1E293B', color: '#F8FAFC', padding: 14, borderRadius: 12, borderWidth: 1, borderColor: '#334155', fontSize: 15 },
  textArea: { height: 120, textAlignVertical: 'top' },
  characterCount: { color: '#64748B', fontSize: 12, marginTop: 6, textAlign: 'right' },
  primaryButton: { backgroundColor: '#38BDF8', borderRadius: 12, padding: 16, alignItems: 'center', marginTop: 24, marginBottom: 40 },
  primaryButtonText: { color: '#0F172A', fontWeight: '700', fontSize: 16 }
});
