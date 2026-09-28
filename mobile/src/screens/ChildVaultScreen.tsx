import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';

export default function ChildVaultScreen() {
  const stories = [
    { id: '1', title: 'The Starlight Blanket', occasion: '🌙 Bedtime Story', duration: '0:22' },
  ];

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.headerEmoji}>✨ 🧸 ✨</Text>
      <Text style={styles.title}>Dad's Storybook</Text>
      <Text style={styles.subtitle}>
        Cozy stories and loving words from Dad, whenever you want to feel close.
      </Text>

      <View style={styles.list}>
        {stories.map((story) => (
          <TouchableOpacity key={story.id} style={styles.storyCard}>
            <View style={styles.iconCircle}>
              <Text style={styles.playArrow}>▶</Text>
            </View>
            <View style={styles.storyInfo}>
              <Text style={styles.storyTitle}>{story.title}</Text>
              <Text style={styles.storyMeta}>{story.occasion} • {story.duration}</Text>
            </View>
          </TouchableOpacity>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0B0F19', padding: 24 },
  headerEmoji: { fontSize: 32, textAlign: 'center', marginTop: 30, marginBottom: 8 },
  title: { fontSize: 26, fontWeight: '800', color: '#F1F5F9', textAlign: 'center', marginBottom: 6 },
  subtitle: { fontSize: 14, color: '#94A3B8', textAlign: 'center', marginBottom: 30, lineHeight: 22 },
  list: { gap: 14 },
  storyCard: { backgroundColor: '#1E293B', flexDirection: 'row', alignItems: 'center', padding: 18, borderRadius: 18, borderWidth: 1, borderColor: '#334155' },
  iconCircle: { width: 44, height: 44, borderRadius: 22, backgroundColor: '#38BDF8', justifyContent: 'center', alignItems: 'center', marginRight: 16 },
  playArrow: { color: '#0F172A', fontSize: 16, fontWeight: 'bold' },
  storyInfo: { flex: 1 },
  storyTitle: { color: '#F8FAFC', fontSize: 16, fontWeight: '700', marginBottom: 4 },
  storyMeta: { color: '#94A3B8', fontSize: 13 }
});
